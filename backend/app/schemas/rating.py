from datetime import datetime
from typing import Optional
from pydantic import BaseModel, conint

class RatingBase(BaseModel):
    activity_key: str
    rating: conint(ge=1, le=5)

class RatingCreate(RatingBase):
    pass

class Rating(RatingBase):
    upload_timestamp: datetime

    class Config:
        orm_mode = True

class ActivityStats(BaseModel):
    activity_key: str
    count: int
    average_rating: float
    total_ratings: int 