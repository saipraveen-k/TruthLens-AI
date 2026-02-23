from sqlalchemy import Column, Integer, String, DateTime, Float, Text, Boolean
from sqlalchemy.sql import func
from app.models.database import Base


class Source(Base):
    __tablename__ = "sources"
    
    source_id = Column(Integer, primary_key=True, index=True)
    domain_name = Column(String(255), unique=True, nullable=False, index=True)
    
    # Reliability metrics
    reliability_score = Column(Float, nullable=True)
    bias_rating = Column(String(50), nullable=True)  # left, center, right, mixed
    factual_reporting = Column(String(50), nullable=True)  # high, medium, low
    
    # Source information
    country = Column(String(10), nullable=True)
    category = Column(String(100), nullable=True)  # news, blog, satire, etc.
    
    # Metadata
    is_active = Column(Boolean, default=True)
    last_checked = Column(DateTime(timezone=True), server_default=func.now())
    notes = Column(Text, nullable=True)
    
    # Counters
    analysis_count = Column(Integer, default=0)
    fake_news_count = Column(Integer, default=0)
    
    def __repr__(self):
        return f"<Source(domain={self.domain_name}, reliability={self.reliability_score})>"
