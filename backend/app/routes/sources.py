from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List, Optional

from app.models.database import get_db
from app.models.source_model import Source
from app.routes.auth import get_current_user, User

router = APIRouter()


# Pydantic models
class SourceResponse(BaseModel):
    source_id: int
    domain_name: str
    reliability_score: Optional[float]
    bias_rating: Optional[str]
    factual_reporting: Optional[str]
    country: Optional[str]
    category: Optional[str]
    analysis_count: int
    fake_news_count: int
    
    class Config:
        from_attributes = True


class SourceCreate(BaseModel):
    domain_name: str
    reliability_score: Optional[float] = None
    bias_rating: Optional[str] = None
    factual_reporting: Optional[str] = None
    country: Optional[str] = None
    category: Optional[str] = None


# Routes
@router.get("/", response_model=List[SourceResponse])
async def get_sources(
    limit: int = 100,
    offset: int = 0,
    search: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Get list of news sources with their reliability scores"""
    
    query = db.query(Source).filter(Source.is_active == True)
    
    if search:
        query = query.filter(Source.domain_name.ilike(f"%{search}%"))
    
    sources = query.order_by(Source.reliability_score.desc()).offset(offset).limit(limit).all()
    
    return sources


@router.get("/{domain_name}", response_model=SourceResponse)
async def get_source_by_domain(
    domain_name: str,
    db: Session = Depends(get_db)
):
    """Get source information by domain name"""
    
    source = db.query(Source).filter(
        Source.domain_name == domain_name.lower(),
        Source.is_active == True
    ).first()
    
    if not source:
        raise HTTPException(
            status_code=404,
            detail="Source not found"
        )
    
    return source


@router.post("/", response_model=SourceResponse)
async def create_source(
    source_data: SourceCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create or update a source (admin only)"""
    
    if current_user.role != "admin":
        raise HTTPException(
            status_code=403,
            detail="Admin access required"
        )
    
    # Check if source already exists
    existing_source = db.query(Source).filter(
        Source.domain_name == source_data.domain_name.lower()
    ).first()
    
    if existing_source:
        # Update existing source
        for field, value in source_data.dict(exclude_unset=True).items():
            setattr(existing_source, field, value)
        
        db.commit()
        db.refresh(existing_source)
        return existing_source
    
    # Create new source
    new_source = Source(
        domain_name=source_data.domain_name.lower(),
        reliability_score=source_data.reliability_score,
        bias_rating=source_data.bias_rating,
        factual_reporting=source_data.factual_reporting,
        country=source_data.country,
        category=source_data.category
    )
    
    db.add(new_source)
    db.commit()
    db.refresh(new_source)
    
    return new_source


@router.get("/stats/overview")
async def get_sources_overview(db: Session = Depends(get_db)):
    """Get overview statistics of sources in database"""
    
    total_sources = db.query(Source).filter(Source.is_active == True).count()
    
    high_reliability = db.query(Source).filter(
        Source.is_active == True,
        Source.reliability_score >= 80
    ).count()
    
    medium_reliability = db.query(Source).filter(
        Source.is_active == True,
        Source.reliability_score >= 50,
        Source.reliability_score < 80
    ).count()
    
    low_reliability = db.query(Source).filter(
        Source.is_active == True,
        Source.reliability_score < 50
    ).count()
    
    bias_distribution = db.query(Source.bias_rating, db.func.count(Source.source_id)).filter(
        Source.is_active == True,
        Source.bias_rating.isnot(None)
    ).group_by(Source.bias_rating).all()
    
    return {
        "total_sources": total_sources,
        "reliability_distribution": {
            "high": high_reliability,
            "medium": medium_reliability,
            "low": low_reliability
        },
        "bias_distribution": dict(bias_distribution)
    }


@router.get("/top/reliable")
async def get_top_reliable_sources(
    limit: int = 20,
    db: Session = Depends(get_db)
):
    """Get top most reliable sources"""
    
    sources = db.query(Source).filter(
        Source.is_active == True,
        Source.reliability_score >= 70
    ).order_by(Source.reliability_score.desc()).limit(limit).all()
    
    return sources


@router.get("/top/unreliable")
async def get_top_unreliable_sources(
    limit: int = 20,
    db: Session = Depends(get_db)
):
    """Get top most unreliable sources"""
    
    sources = db.query(Source).filter(
        Source.is_active == True,
        Source.reliability_score <= 30
    ).order_by(Source.reliability_score.asc()).limit(limit).all()
    
    return sources
