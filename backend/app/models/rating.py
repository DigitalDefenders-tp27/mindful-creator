from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from app.database import Base

class Rating(Base):
    """
    Database model for activity ratings.
    
    This model maps to the activity_rating_counts table in the database and stores
    user-provided ratings for various mindfulness activities. Each record 
    represents a single user rating for a specific activity type.
    
    The table includes:
    - A unique ID (primary key)
    - The activity type being rated
    - The numerical rating value
    - A timestamp when the rating was created
    - A user ID (optional)
    """
    __tablename__ = "activity_rating_counts"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    activity_type = Column(String, index=True, nullable=False)
    rating_value = Column(Integer, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    user_id = Column(Integer, nullable=True)

    # Make our model flexible to allow access via both naming conventions
    @property
    def activity_key(self):
        return self.activity_type
        
    @activity_key.setter
    def activity_key(self, value):
        self.activity_type = value
        
    @property
    def rating(self):
        return self.rating_value
        
    @rating.setter
    def rating(self, value):
        self.rating_value = value

    class Config:
        orm_mode = True 