# backend/database.py
import os
import psycopg2
from dotenv import load_dotenv
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

load_dotenv()


# Get database URL from environment variable or use default SQLite database
DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///./relaxation.db')

# Create database engine
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

class ActivityRating(Base):
    __tablename__ = "activity_ratings"

    id = Column(Integer, primary_key=True, index=True)
    activity = Column(String, index=True)
    rating = Column(Integer)
    timestamp = Column(DateTime, default=datetime.utcnow)

# Create all tables
Base.metadata.create_all(bind=engine)

# Database dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Database operations
def get_activity_ratings_count(db, activity: str) -> int:
    return db.query(ActivityRating).filter(ActivityRating.activity == activity).count()

def create_activity_rating(db, activity: str, rating: int):
    db_rating = ActivityRating(
        activity=activity,
        rating=rating
    )
    db.add(db_rating)
    db.commit()
    db.refresh(db_rating)
    return db_rating

def get_connection():
    DATABASE_URL = os.getenv("DATABASE_URL")
    if not DATABASE_URL:
        raise RuntimeError("DATABASE_URL environment variable is not set")
    return psycopg2.connect(dsn=DATABASE_URL, sslmode="require")

