from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from app.database import Base

class Rating(Base):
    """
    Database model for activity ratings.
    Maps to the activity_ratings table in the database.
    """
    __tablename__ = "activity_ratings"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    activity_type = Column(String, index=True, nullable=False)
    rating_value = Column(Integer, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    class Config:
        orm_mode = True 