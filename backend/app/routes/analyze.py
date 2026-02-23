from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional, Dict, Any
import uuid
import hashlib
import time
from datetime import datetime

from app.models.database import get_db
from app.models.article_model import Article
from app.models.cache_model import AnalysisCache
from app.routes.auth import get_current_user, User
from app.services.nlp_pipeline import NLPipeline
from app.services.web_scraper import WebScraper
from app.utils.validators import validate_text_input, validate_url
from app.config import settings

router = APIRouter()


# Pydantic models
class TextAnalysisRequest(BaseModel):
    text: str
    language: Optional[str] = None


class URLAnalysisRequest(BaseModel):
    url: str
    extract_full_text: Optional[bool] = True


class AnalysisResponse(BaseModel):
    article_id: str
    credibility_score: float
    fake_probability: float
    bias_score: str
    emotional_manipulation: str
    source_reliability: str
    analysis: Dict[str, Any]
    explanation: Dict[str, Any]
    source_info: Dict[str, Any]
    metadata: Dict[str, Any]


# Helper functions
def generate_content_hash(text: str) -> str:
    """Generate SHA-256 hash for content caching"""
    return hashlib.sha256(text.encode()).hexdigest()


def get_cached_analysis(content_hash: str, db: Session) -> Optional[Dict[str, Any]]:
    """Get cached analysis result"""
    cache = db.query(AnalysisCache).filter(
        AnalysisCache.content_hash == content_hash
    ).first()
    
    if cache and cache.expires_at and cache.expires_at > datetime.utcnow():
        return cache.analysis_result
    
    return None


def cache_analysis_result(content_hash: str, result: Dict[str, Any], db: Session):
    """Cache analysis result"""
    cache = AnalysisCache(
        content_hash=content_hash,
        analysis_result=result,
        language=result.get("metadata", {}).get("language", "en")
    )
    
    db.add(cache)
    db.commit()


# Routes
@router.post("/text", response_model=AnalysisResponse)
async def analyze_text(
    request: TextAnalysisRequest,
    current_user: Optional[User] = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Analyze text for credibility"""
    
    # Validate input
    validated_text = validate_text_input(request.text)
    
    # Generate content hash for caching
    content_hash = generate_content_hash(validated_text)
    
    # Check cache first
    cached_result = get_cached_analysis(content_hash, db)
    if cached_result:
        return AnalysisResponse(**cached_result)
    
    # Get NLP pipeline from app state
    from app.main import app
    nlp_pipeline: NLPipeline = app.state.nlp_pipeline
    
    # Perform analysis
    start_time = time.time()
    analysis_result = await nlp_pipeline.analyze_text(
        text=validated_text,
        language=request.language or settings.default_language
    )
    processing_time = time.time() - start_time
    
    # Create article record
    article_id = str(uuid.uuid4())
    article = Article(
        article_id=article_id,
        user_id=current_user.user_id if current_user else None,
        content=validated_text,
        credibility_score=analysis_result["credibility_score"],
        fake_probability=analysis_result["fake_probability"],
        bias_score=analysis_result["bias_score"],
        emotional_manipulation=analysis_result["emotional_manipulation"],
        source_reliability=analysis_result["source_reliability"],
        analysis_result=analysis_result["analysis"],
        explanation=analysis_result["explanation"],
        language=analysis_result.get("metadata", {}).get("language", "en"),
        word_count=len(validated_text.split()),
        processing_time=processing_time
    )
    
    db.add(article)
    db.commit()
    
    # Prepare response
    response_data = {
        "article_id": article_id,
        **analysis_result
    }
    
    # Cache the result
    cache_analysis_result(content_hash, response_data, db)
    
    return AnalysisResponse(**response_data)


@router.post("/url", response_model=AnalysisResponse)
async def analyze_url(
    request: URLAnalysisRequest,
    current_user: Optional[User] = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Analyze article from URL"""
    
    # Validate URL
    validated_url = validate_url(request.url)
    
    # Extract content from URL
    scraper = WebScraper()
    try:
        article_data = await scraper.extract_article(validated_url, request.extract_full_text)
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Failed to extract content from URL: {str(e)}"
        )
    
    if not article_data.get("content"):
        raise HTTPException(
            status_code=400,
            detail="Could not extract content from the provided URL"
        )
    
    # Generate content hash for caching
    content_hash = generate_content_hash(article_data["content"])
    
    # Check cache first
    cached_result = get_cached_analysis(content_hash, db)
    if cached_result:
        return AnalysisResponse(**cached_result)
    
    # Get NLP pipeline from app state
    from app.main import app
    nlp_pipeline: NLPipeline = app.state.nlp_pipeline
    
    # Perform analysis
    start_time = time.time()
    analysis_result = await nlp_pipeline.analyze_text(
        text=article_data["content"],
        language=settings.default_language
    )
    processing_time = time.time() - start_time
    
    # Create article record
    article_id = str(uuid.uuid4())
    article = Article(
        article_id=article_id,
        user_id=current_user.user_id if current_user else None,
        title=article_data.get("title"),
        content=article_data["content"],
        url=validated_url,
        credibility_score=analysis_result["credibility_score"],
        fake_probability=analysis_result["fake_probability"],
        bias_score=analysis_result["bias_score"],
        emotional_manipulation=analysis_result["emotional_manipulation"],
        source_reliability=analysis_result["source_reliability"],
        analysis_result=analysis_result["analysis"],
        explanation=analysis_result["explanation"],
        language=analysis_result.get("metadata", {}).get("language", "en"),
        word_count=len(article_data["content"].split()),
        processing_time=processing_time
    )
    
    db.add(article)
    db.commit()
    
    # Add source information to response
    source_info = {
        "domain": scraper.get_domain(validated_url),
        "url": validated_url,
        "title": article_data.get("title"),
        "author": article_data.get("author"),
        "publish_date": article_data.get("publish_date"),
        "reliability_score": analysis_result.get("source_reliability_score"),
        "notes": "Extracted from provided URL"
    }
    
    # Prepare response
    response_data = {
        "article_id": article_id,
        **analysis_result,
        "source_info": source_info
    }
    
    # Cache the result
    cache_analysis_result(content_hash, response_data, db)
    
    return AnalysisResponse(**response_data)


@router.post("/pdf", response_model=AnalysisResponse)
async def analyze_pdf(
    file: UploadFile = File(...),
    current_user: Optional[User] = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Analyze PDF file for credibility"""
    
    # Validate file
    if not file.filename.lower().endswith('.pdf'):
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are allowed"
        )
    
    if file.size > settings.max_file_size:
        raise HTTPException(
            status_code=400,
            detail=f"File size exceeds maximum limit of {settings.max_file_size} bytes"
        )
    
    # Extract text from PDF
    try:
        import PyPDF2
        import io
        
        # Read file content
        content = await file.read()
        pdf_reader = PyPDF2.PdfReader(io.BytesIO(content))
        
        # Extract text from all pages
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text() + "\n"
        
        if not text.strip():
            raise HTTPException(
                status_code=400,
                detail="Could not extract text from PDF file"
            )
    
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Failed to process PDF file: {str(e)}"
        )
    
    # Generate content hash for caching
    content_hash = generate_content_hash(text)
    
    # Check cache first
    cached_result = get_cached_analysis(content_hash, db)
    if cached_result:
        return AnalysisResponse(**cached_result)
    
    # Get NLP pipeline from app state
    from app.main import app
    nlp_pipeline: NLPipeline = app.state.nlp_pipeline
    
    # Perform analysis
    start_time = time.time()
    analysis_result = await nlp_pipeline.analyze_text(
        text=text,
        language=settings.default_language
    )
    processing_time = time.time() - start_time
    
    # Create article record
    article_id = str(uuid.uuid4())
    article = Article(
        article_id=article_id,
        user_id=current_user.user_id if current_user else None,
        title=file.filename.replace('.pdf', ''),
        content=text,
        credibility_score=analysis_result["credibility_score"],
        fake_probability=analysis_result["fake_probability"],
        bias_score=analysis_result["bias_score"],
        emotional_manipulation=analysis_result["emotional_manipulation"],
        source_reliability=analysis_result["source_reliability"],
        analysis_result=analysis_result["analysis"],
        explanation=analysis_result["explanation"],
        language=analysis_result.get("metadata", {}).get("language", "en"),
        word_count=len(text.split()),
        processing_time=processing_time
    )
    
    db.add(article)
    db.commit()
    
    # Add source information to response
    source_info = {
        "domain": None,
        "url": None,
        "title": file.filename.replace('.pdf', ''),
        "author": None,
        "publish_date": None,
        "reliability_score": None,
        "notes": "Extracted from uploaded PDF file"
    }
    
    # Prepare response
    response_data = {
        "article_id": article_id,
        **analysis_result,
        "source_info": source_info
    }
    
    # Cache the result
    cache_analysis_result(content_hash, response_data, db)
    
    return AnalysisResponse(**response_data)


@router.get("/history")
async def get_analysis_history(
    limit: int = 50,
    offset: int = 0,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get user's analysis history"""
    
    articles = db.query(Article).filter(
        Article.user_id == current_user.user_id
    ).order_by(Article.created_at.desc()).offset(offset).limit(limit).all()
    
    return {
        "articles": [
            {
                "article_id": article.article_id,
                "title": article.title,
                "credibility_score": article.credibility_score,
                "fake_probability": article.fake_probability,
                "bias_score": article.bias_score,
                "created_at": article.created_at,
                "word_count": article.word_count
            }
            for article in articles
        ],
        "total": len(articles)
    }


@router.get("/article/{article_id}")
async def get_article_analysis(
    article_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get detailed analysis for a specific article"""
    
    article = db.query(Article).filter(
        Article.article_id == article_id,
        Article.user_id == current_user.user_id
    ).first()
    
    if not article:
        raise HTTPException(
            status_code=404,
            detail="Article not found"
        )
    
    return {
        "article_id": article.article_id,
        "title": article.title,
        "content": article.content,
        "url": article.url,
        "credibility_score": article.credibility_score,
        "fake_probability": article.fake_probability,
        "bias_score": article.bias_score,
        "emotional_manipulation": article.emotional_manipulation,
        "source_reliability": article.source_reliability,
        "analysis": article.analysis_result,
        "explanation": article.explanation,
        "metadata": {
            "language": article.language,
            "word_count": article.word_count,
            "processing_time": article.processing_time,
            "created_at": article.created_at
        }
    }
