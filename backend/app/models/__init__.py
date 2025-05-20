"""
Models package for SQLAlchemy ORM models.

This package contains all database model definitions using SQLAlchemy ORM.
Models defined here are automatically mapped to database tables.
"""

from app.models.rating import Rating
from app.models.meme import MemeFetch
from sqlalchemy import Column, Integer, String
from app.database import Base

# Define TrainCleaned here to avoid circular imports
class TrainCleaned(Base):
    """
    Database model for train_cleaned table.
    Contains cleaned training data.
    """
    __tablename__ = "train_cleaned"

    User_ID = Column(Integer, primary_key=True, index=True)
    Age = Column(Integer)
    Gender = Column(String)
    Platform = Column(String)
    daily_usage_time = Column(Integer)
    posts_per_day = Column(Integer)
    likes_received_per_day = Column(Integer)
    comments_received_per_day = Column(Integer)
    messages_sent_per_day = Column(Integer)
    dominant_emotion = Column(String)

# Export all models for convenient importing
__all__ = [
    "Rating",       # User ratings for activities
    "MemeFetch",    # Meme data for memory match game
    "TrainCleaned"  # Train dataset cleaned records
] 