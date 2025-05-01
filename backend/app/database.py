from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.database import get_connection
import os

# Load DB URL from .env
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://username:password@host:port/dbname")

# SQLAlchemy setup
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class to inherit models from
Base = declarative_base()

# Dependency for FastAPI
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Pull in the psycopg2‐based connection helper
from backend.database import get_connection
