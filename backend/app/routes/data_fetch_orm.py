from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import TrainCleaned
from collections import defaultdict

router = APIRouter()

@router.get("/screen-time-emotions")
def get_emotion_distribution_by_screen_time(db: Session = Depends(get_db)):
    data = db.query(TrainCleaned.daily_usage_time, TrainCleaned.dominant_emotion).all()

    # Define screen time groups in hours
    def categorize_screen_time(minutes):
        if minutes < 60:
            return "0-1 hrs"
        elif minutes < 120:
            return "1-2 hrs"
        elif minutes < 180:
            return "2-3 hrs"
        elif minutes < 240:
            return "3-4 hrs"
        else:
            return "4+ hrs"

    # Group counts
    group_counts = defaultdict(lambda: defaultdict(int))
    total_per_group = defaultdict(int)

    for time, emotion in data:
        group = categorize_screen_time(time)
        group_counts[group][emotion] += 1
        total_per_group[group] += 1

    # Calculate percentages
    response = []
    for group in group_counts:
        for emotion in group_counts[group]:
            percentage = (group_counts[group][emotion] / total_per_group[group]) * 100
            response.append({
                "screen_time_group": group,
                "dominant_emotion": emotion,
                "percentage": round(percentage, 2)
            })

    # Sort results by screen time group order
    sort_order = {"0-1 hrs": 0, "1-2 hrs": 1, "2-3 hrs": 2, "3-4 hrs": 3, "4+ hrs": 4}
    response = sorted(response, key=lambda x: sort_order.get(x["screen_time_group"], 99))

    return response
