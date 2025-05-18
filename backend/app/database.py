from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
import re
from dotenv import load_dotenv

load_dotenv()

# Get DATABASE_URL from environment variable
raw_database_url = os.getenv("DATABASE_URL", "sqlite:///./relaxation.db")

# Handle Railway PostgreSQL URLs if provided
if raw_database_url and "postgres" in raw_database_url:
    # If it's just a hostname, convert it to a proper URL format
    if not raw_database_url.startswith("postgresql://"):
        # Default to a standard format if only the hostname is provided
        DATABASE_URL = f"postgresql://postgres:postgres@{raw_database_url}:5432/railway"
    else:
        # If it's a full URL but potentially has the "postgres://" prefix (which SQLAlchemy doesn't support)
        DATABASE_URL = raw_database_url.replace("postgres://", "postgresql://")
    
    # Create database engine with PostgreSQL-specific pool settings
    engine = create_engine(
        DATABASE_URL,
        pool_size=5,
        max_overflow=10,
        pool_timeout=30,
        pool_recycle=1800
    )
else:
    # SQLite doesn't support pooling parameters
    DATABASE_URL = raw_database_url
    engine = create_engine(DATABASE_URL)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create base class
Base = declarative_base()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Create tables
def create_tables():
    Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    create_tables()
    print("Database tables created successfully!")

# Import for backwards compatibility
try:
    from backend.database import get_connection
except ImportError:
    # Fallback implementation if needed
    def get_connection():
        """Fallback implementation of get_connection"""
        pass
