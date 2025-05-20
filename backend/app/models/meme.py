from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.sql import func
from app.database import Base
from typing import Optional

class MemeFetch(Base):
    """
    Database model for meme fetching.
    Maps to the meme_fetch table in the database.
    """
    __tablename__ = "meme_fetch"

    # Based on the SQL query, using the same column names
    # If there's a need for a primary key that isn't apparent from the SQL,
    # you may need to adjust this model
    image_name = Column(String, primary_key=True, index=True)
    humour = Column(String, nullable=True)
    sarcasm = Column(String, nullable=True)
    offensive = Column(String, nullable=True)
    motivational = Column(String, nullable=True)
    overall_sentiment = Column(String, nullable=True)

    class Config:
        orm_mode = True 