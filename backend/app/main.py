from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
import logging
import time
import uvicorn

from app.config import settings
from app.routes import auth, analyze, sources
from app.models.database import engine, Base


# Configure logging
logging.basicConfig(
    level=getattr(logging, settings.log_level),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(settings.log_file),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    logger.info("Starting TruthLens AI Backend...")
    
    # Create database tables
    Base.metadata.create_all(bind=engine)
    logger.info("Database tables created successfully")
    
    # Load ML models
    try:
        from app.services.nlp_pipeline import NLPipeline
        nlp_pipeline = NLPipeline()
        await nlp_pipeline.initialize()
        app.state.nlp_pipeline = nlp_pipeline
        logger.info("ML models loaded successfully")
    except Exception as e:
        logger.error(f"Failed to load ML models: {e}")
        raise
    
    yield
    
    # Shutdown
    logger.info("Shutting down TruthLens AI Backend...")


# Create FastAPI app
app = FastAPI(
    title=settings.app_name,
    description="AI-powered news credibility analyzer with bias detection and emotional manipulation analysis",
    version=settings.version,
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add trusted host middleware
app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=["localhost", "127.0.0.1", "*"]
)


# Request timing middleware
@app.middleware("http")
async def add_process_time_header(request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response


# Include routers
app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(analyze.router, prefix="/analyze", tags=["Analysis"])
app.include_router(sources.router, prefix="/sources", tags=["Sources"])


# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "version": settings.version,
        "app_name": settings.app_name,
        "features": {
            "multilingual": settings.enable_multilingual,
            "browser_extension": settings.enable_browser_extension,
            "real_time_analysis": settings.enable_real_time_analysis
        }
    }


# Root endpoint
@app.get("/")
async def root():
    """Root endpoint with API info"""
    return {
        "message": "Welcome to TruthLens AI API",
        "version": settings.version,
        "docs": "/docs",
        "health": "/health"
    }


# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    logger.error(f"Global exception: {exc}")
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
            "message": "Something went wrong. Please try again later.",
            "details": str(exc) if settings.debug else None
        }
    )


if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.debug,
        log_level=settings.log_level.lower()
    )
