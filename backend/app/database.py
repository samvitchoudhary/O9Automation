"""
Database setup and initialization for O9 Test Automation Platform
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()

# Database URL from environment or default to SQLite
# Use absolute path to avoid permission issues
base_dir = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(base_dir, '..', 'test_cases.db')
db_path = os.path.abspath(db_path)

# Ensure the directory exists and is writable
db_dir = os.path.dirname(db_path)
os.makedirs(db_dir, exist_ok=True)
# Make directory writable
try:
    os.chmod(db_dir, 0o755)
except:
    pass

DATABASE_URL = os.getenv("DATABASE_URL", f"sqlite:///{db_path}")

# Create engine with proper SQLite configuration
connect_args = {}
if "sqlite" in DATABASE_URL:
    connect_args = {
        "check_same_thread": False,
        "timeout": 20  # Increase timeout for concurrent access
    }

engine = create_engine(
    DATABASE_URL,
    connect_args=connect_args,
    pool_pre_ping=True  # Verify connections before using
)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for models
Base = declarative_base()


def init_db():
    """Initialize the database by creating all tables"""
    from app.models import TestCase, TestStep
    Base.metadata.create_all(bind=engine)
    print("Database initialized successfully!")


def get_db():
    """Dependency for getting database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

