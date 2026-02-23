from sqlalchemy import Column, Integer, String, DateTime, JSON
from sqlalchemy.sql import func
from app.models.database import Base


class AnalysisCache(Base):
    __tablename__ = "analysis_cache"
    
    cache_id = Column(Integer, primary_key=True, index=True)
    content_hash = Column(String(64), unique=True, nullable=False, index=True)
    analysis_result = Column(JSON, nullable=False)
    language = Column(String(10), default="en")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    expires_at = Column(DateTime(timezone=True), nullable=True)
    
    def __repr__(self):
        return f"<AnalysisCache(hash={self.content_hash[:8]}..., expires={self.expires_at})>"
