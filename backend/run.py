"""
Main entry point for the O9 Test Automation Platform backend
"""
import uvicorn
import os
import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import router
from app.database import init_db
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set up logging
logging.basicConfig(
    level=logging.INFO, 
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="O9 Test Automation Platform API",
    description="API for automating O9 supply chain testing",
    version="1.0.0"
)

# Configure CORS - CRITICAL FIX
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",  # Vite dev server
        "http://127.0.0.1:5173",
        "http://localhost:3000",  # React default
        "http://127.0.0.1:3000",
        "http://localhost:8000",  # Backend itself
        "http://127.0.0.1:8000"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routes
app.include_router(router)


@app.on_event("startup")
async def startup_event():
    """Initialize database on startup"""
    logger.info("=" * 60)
    logger.info("Starting O9 Test Automation Platform Backend")
    logger.info("=" * 60)
    
    # Initialize database
    init_db()
    logger.info("✓ Database initialized")
    
    # Verify API key is loaded
    api_key = os.getenv('ANTHROPIC_API_KEY')
    if not api_key:
        logger.warning("⚠️  ANTHROPIC_API_KEY not found in environment!")
        logger.warning("   Selenium script generation will not work without it.")
        logger.warning("   Create backend/.env file with your API key")
    else:
        logger.info(f"✓ ANTHROPIC_API_KEY loaded (starts with: {api_key[:15]}...)")
    
    # Check mock O9 URL
    mock_url = os.getenv('O9_MOCK_URL', 'http://localhost:3001')
    logger.info(f"✓ Mock O9 URL configured: {mock_url}")
    
    logger.info("=" * 60)
    logger.info("Backend is ready!")
    logger.info("API Docs: http://localhost:8000/docs")
    logger.info("=" * 60)


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "O9 Test Automation Platform API",
        "version": "1.0.0",
        "status": "running",
        "docs": "/docs"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "api_key_configured": bool(os.getenv('ANTHROPIC_API_KEY'))
    }


if __name__ == "__main__":
    # Run with uvicorn
    logger.info("Starting server with uvicorn...")
    uvicorn.run(
        "run:app", 
        host="0.0.0.0", 
        port=8000, 
        reload=True,
        log_level="info"
    )

