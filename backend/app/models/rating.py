from sqlalchemy import Column, Integer, String, DateTime, Enum
from sqlalchemy.sql import func
from app.database import Base

class Rating(Base):
    __tablename__ = "activity_ratings"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    activity_key = Column(String, index=True, nullable=False)
    rating = Column(Integer, nullable=False)
    upload_timestamp = Column(DateTime(timezone=True), server_default=func.now())

    class Config:
        orm_mode = True 