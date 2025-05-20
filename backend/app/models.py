from sqlalchemy import Column, Integer, String
from app.database import Base

class TrainCleaned(Base):
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

class Rating(Base):
    __tablename__ = "ratings"

    id = Column(Integer, primary_key=True, index=True)
    comment_id = Column(Integer)
    rating = Column(Integer)