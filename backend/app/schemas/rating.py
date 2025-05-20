from datetime import datetime
from typing import Optional
from pydantic import BaseModel, conint

class RatingBase(BaseModel):
    activity_key: str
    rating: conint(ge=1, le=5)

class RatingCreate(RatingBase):
    pass

class Rating(RatingBase):
    id: int
    activity_type: str
    rating_value: int
    created_at: datetime

    class Config:
        orm_mode = True
        fields = {
            'activity_type': {'alias': 'activity_key'},
            'rating_value': {'alias': 'rating'}
        }

class ActivityStats(BaseModel):
    activity_key: str
    count: int
    average_rating: float
    total_ratings: int 