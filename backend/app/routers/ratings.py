from fastapi import APIRouter, Depends, HTTPException, Request, Response
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Dict, Any
from app.database import get_db
from app.models import Rating
from app.schemas.rating import RatingCreate, Rating as RatingSchema, ActivityStats
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

# OPTIONS method to support preflight requests
@router.options("/{path:path}")
async def options_ratings_all_paths():
    return Response(status_code=200)

@router.post("/")
def create_rating(rating: RatingCreate, db: Session = Depends(get_db)):
    try:
        logger.info(f"Received new rating: activity_key={rating.activity_key}, rating={rating.rating}")
        
        # Create new rating record
        db_rating = Rating(
            activity_key=rating.activity_key,
            rating=rating.rating
        )
        db.add(db_rating)
        db.commit()
        db.refresh(db_rating)
        logger.info(f"Successfully saved rating ID={db_rating.id}")
        
        # Get updated statistics for this activity
        stats = db.query(
            Rating.activity_key,
            func.count(Rating.id).label("count"),
            func.avg(Rating.rating).label("average_rating"),
            func.count(Rating.id).label("total_ratings")
        ).filter(
            Rating.activity_key == rating.activity_key
        ).group_by(
            Rating.activity_key
        ).first()
        
        if not stats:
            logger.warning(f"No statistics found for activity {rating.activity_key}, this should be the first rating for this activity")
            return {
                "rating": {
                    "id": db_rating.id,
                    "activity_key": db_rating.activity_key,
                    "rating": db_rating.rating
                },
                "stats": {
                    "activity_key": rating.activity_key,
                    "count": 1,
                    "average_rating": float(rating.rating),
                    "total_ratings": 1
                }
            }
        
        logger.info(f"Statistics for activity {rating.activity_key}: count={stats[1]}, avg={stats[2]}, total={stats[3]}")
        return {
            "rating": {
                "id": db_rating.id,
                "activity_key": db_rating.activity_key,
                "rating": db_rating.rating
            },
            "stats": {
                "activity_key": stats[0],
                "count": stats[1],
                "average_rating": float(stats[2] or 0),
                "total_ratings": stats[3]
            }
        }
    except Exception as e:
        logger.error(f"Error while creating rating: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error while creating rating: {str(e)}")

@router.put("/")
def update_rating(rating: RatingCreate, db: Session = Depends(get_db)):
    return create_rating(rating, db)

@router.post("/{id}")
def create_rating_with_id(id: str, rating: RatingCreate, db: Session = Depends(get_db)):
    return create_rating(rating, db)

@router.put("/{id}")
def update_rating_with_id(id: str, rating: RatingCreate, db: Session = Depends(get_db)):
    return create_rating(rating, db)

@router.get("/")
def get_all_stats(db: Session = Depends(get_db)):
    try:
        logger.info("Getting statistics for all activities")
        stats = db.query(
            Rating.activity_key,
            func.count(Rating.id).label("count"),
            func.avg(Rating.rating).label("average_rating"),
            func.count(Rating.id).label("total_ratings")
        ).group_by(
            Rating.activity_key
        ).all()
        
        logger.info(f"Found statistics for {len(stats)} activities")
        return [
            ActivityStats(
                activity_key=stat[0],
                count=stat[1],
                average_rating=float(stat[2] or 0),
                total_ratings=stat[3]
            )
            for stat in stats
        ]
    except Exception as e:
        logger.error(f"Error while getting all statistics: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error while getting statistics: {str(e)}")

@router.get("/{activity_key}", response_model=ActivityStats)
def get_activity_stats(activity_key: str, db: Session = Depends(get_db)):
    try:
        logger.info(f"Getting statistics for activity {activity_key}")
        
        # Special path handling
        if activity_key.startswith(":") or activity_key == "1":
            logger.info(f"Detected special path {activity_key}, returning default empty statistics")
            return ActivityStats(
                activity_key="default",
                count=0,
                average_rating=0.0,
                total_ratings=0
            )
            
        # Query database
        stats = db.query(
            Rating.activity_key,
            func.count(Rating.id).label("count"),
            func.avg(Rating.rating).label("average_rating"),
            func.count(Rating.id).label("total_ratings")
        ).filter(
            Rating.activity_key == activity_key
        ).group_by(
            Rating.activity_key
        ).first()
        
        if not stats:
            logger.info(f"No statistics found for activity {activity_key}")
            return ActivityStats(
                activity_key=activity_key,
                count=0,
                average_rating=0.0,
                total_ratings=0
            )
        
        logger.info(f"Found statistics for activity {activity_key}: count={stats[1]}, avg={stats[2]}, total={stats[3]}")
        return ActivityStats(
            activity_key=stats[0],
            count=stats[1],
            average_rating=float(stats[2] or 0),
            total_ratings=stats[3]
        )
    except Exception as e:
        logger.error(f"Error while getting statistics for activity {activity_key}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error while getting statistics: {str(e)}") 