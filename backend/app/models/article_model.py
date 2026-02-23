from sqlalchemy import Column, Integer, String, DateTime, Float, Text, Boolean, ForeignKey, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.models.database import Base


class Article(Base):
    __tablename__ = "articles"
    
    article_id = Column(String(36), primary_key=True, index=True)  # UUID
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=True)
    title = Column(String(500), nullable=True)
    content = Column(Text, nullable=False)
    url = Column(String(1000), nullable=True)
    
    # Analysis results
    credibility_score = Column(Float, nullable=True)
    fake_probability = Column(Float, nullable=True)
    bias_score = Column(String(50), nullable=True)
    emotional_manipulation = Column(String(50), nullable=True)
    source_reliability = Column(String(50), nullable=True)
    
    # Detailed analysis (JSON)
    analysis_result = Column(JSON, nullable=True)
    explanation = Column(JSON, nullable=True)
    
    # Metadata
    language = Column(String(10), default="en")
    word_count = Column(Integer, nullable=True)
    processing_time = Column(Float, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    user = relationship("User", back_populates="articles")
    
    def __repr__(self):
        return f"<Article(id={self.article_id}, credibility={self.credibility_score})>"
