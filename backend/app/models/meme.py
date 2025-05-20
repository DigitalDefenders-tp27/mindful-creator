from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.sql import func
from app.database import Base
from typing import Optional

class MemeFetch(Base):
    """
    SQLAlchemy database model for meme fetching.
    
    This model maps to the meme_fetch table in the database and is used 
    for retrieving meme data for the memory match game. It contains
    sentiment analysis attributes of each meme.
    
    The image_name serves as the primary key, linking to the actual image files
    stored in the meme_images directory.
    """
    __tablename__ = "meme_fetch"

    # Using the existing column names from the database table
    # The image_name is set as the primary key to uniquely identify each meme
    image_name = Column(String, primary_key=True, index=True)
    
    # Sentiment analysis attributes
    humour = Column(String, nullable=True)  # Australian spelling for humor
    sarcasm = Column(String, nullable=True)
    offensive = Column(String, nullable=True)
    motivational = Column(String, nullable=True)
    overall_sentiment = Column(String, nullable=True)

    class Config:
        orm_mode = True 