from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from app.database import Base

class Rating(Base):
    """
    Database model for activity ratings.
    
    This model maps to the activity_ratings table in the database and stores
    user-provided ratings for various mindfulness activities. Each record 
    represents a single user rating for a specific activity type.
    
    The table includes:
    - A unique ID (primary key)
    - The activity type being rated
    - The numerical rating value
    - A timestamp when the rating was created
    """
    __tablename__ = "activity_ratings"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    activity_type = Column(String, index=True, nullable=False)
    rating_value = Column(Integer, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    class Config:
        orm_mode = True 