from pydantic_settings import BaseSettings
from typing import List
import os


class Settings(BaseSettings):
    # Application
    app_name: str = "TruthLens AI"
    version: str = "1.0.0"
    debug: bool = False
    secret_key: str
    
    # Database
    db_host: str = "localhost"
    db_port: int = 5432
    db_name: str = "truthlens_db"
    db_user: str = "postgres"
    db_password: str = "postgres"
    
    @property
    def database_url(self) -> str:
        return f"postgresql://{self.db_user}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_name}"
    
    # API Keys
    news_api_key: str = ""
    google_translate_api_key: str = ""
    huggingface_api_key: str = ""
    
    # Model Paths
    bert_model_path: str = "./models_training/saved_models/bert_fake_news.pt"
    lstm_model_path: str = "./models_training/saved_models/lstm_fake_news.h5"
    baseline_model_path: str = "./models_training/saved_models/baseline_model.pkl"
    
    # Processing
    max_text_length: int = 10000
    default_language: str = "en"
    supported_languages: List[str] = ["en", "hi", "es", "fr", "de"]
    
    # Cache
    redis_url: str = "redis://localhost:6379/0"
    cache_ttl: int = 3600
    
    # File Upload
    max_file_size: int = 10485760  # 10MB
    upload_dir: str = "./uploads"
    
    # CORS
    allowed_origins: List[str] = ["http://localhost:3000", "http://127.0.0.1:3000"]
    
    # Logging
    log_level: str = "INFO"
    log_file: str = "./logs/app.log"
    
    # Rate Limiting
    rate_limit_per_minute: int = 60
    
    # Feature Flags
    enable_multilingual: bool = True
    enable_browser_extension: bool = True
    enable_real_time_analysis: bool = False
    
    class Config:
        env_file = ".env"
        case_sensitive = False


# Create global settings instance
settings = Settings()

# Ensure upload directory exists
os.makedirs(settings.upload_dir, exist_ok=True)
os.makedirs(os.path.dirname(settings.log_file), exist_ok=True)
