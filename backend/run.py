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
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="O9 Test Automation Platform API",
    description="API for automating O9 supply chain testing",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],  # Vite default port
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routes
app.include_router(router)


@app.on_event("startup")
async def startup_event():
    """Initialize database on startup"""
    init_db()
    
    # Verify API key is loaded
    api_key = os.getenv('ANTHROPIC_API_KEY')
    if not api_key:
        logger.warning("⚠️  ANTHROPIC_API_KEY not found in environment!")
        logger.warning("   Selenium script generation will not work without it.")
    else:
        logger.info(f"✓ ANTHROPIC_API_KEY loaded (starts with: {api_key[:10]}...)")


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "O9 Test Automation Platform API",
        "version": "1.0.0",
        "docs": "/docs"
    }


if __name__ == "__main__":
    uvicorn.run("run:app", host="0.0.0.0", port=8000, reload=True)

