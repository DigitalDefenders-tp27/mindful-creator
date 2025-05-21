from fastapi import APIRouter, Depends, HTTPException, Request, Response
from sqlalchemy.orm import Session
from sqlalchemy import func, text
from typing import List, Dict, Any
from app.database import get_db, SessionLocal
from app.models.rating import Rating
from app.schemas.rating import RatingCreate, Rating as RatingSchema, ActivityStats
import logging
import traceback
import json

router = APIRouter()
logger = logging.getLogger(__name__)

# Helper function to add CORS headers to responses
def add_cors_headers(response: Response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
    return response

# Helper function to get a DB session directly (not as a generator)
def get_db_session():
    """
    Get a direct database session without using the generator.
    This is a workaround for the 'generator' object has no attribute 'query' error.
    """
    db = SessionLocal()
    try:
        return db
    except Exception as e:
        db.close()
        logger.error(f"Error getting direct DB session: {str(e)}")
        raise

# OPTIONS method to support preflight requests
@router.options("/{path:path}")
async def options_ratings_all_paths():
    response = Response(status_code=200)
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
    return response

@router.get("/debug")
async def debug_database(db: Session = Depends(get_db)):
    """Debugging endpoint to check database connection and tables"""
    try:
        # Try a simple query first
        result = db.execute(text("SELECT 1")).fetchone()
        logger.info(f"Basic SELECT query result: {result}")
        
        # Try to list tables
        try:
            if 'postgresql' in db.bind.dialect.name:
                tables = db.execute(text("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'")).fetchall()
            else:  # SQLite
                tables = db.execute(text("SELECT name FROM sqlite_master WHERE type='table'")).fetchall()
            
            logger.info(f"Tables in database: {tables}")
            
            # Check the activity_rating_counts table structure
            try:
                if 'activity_rating_counts' in [t[0] for t in tables]:
                    if 'postgresql' in db.bind.dialect.name:
                        columns = db.execute(text("SELECT column_name, data_type FROM information_schema.columns WHERE table_name = 'activity_rating_counts'")).fetchall()
                    else:  # SQLite
                        columns = db.execute(text("PRAGMA table_info(activity_rating_counts)")).fetchall()
                    
                    logger.info(f"activity_rating_counts columns: {columns}")
                    return {
                        "status": "success", 
                        "message": "Database connection working",
                        "tables": [t[0] for t in tables],
                        "activity_rating_counts_columns": columns
                    }
                else:
                    return {
                        "status": "warning",
                        "message": "activity_rating_counts table not found",
                        "tables": [t[0] for t in tables]
                    }
            except Exception as e:
                logger.error(f"Error checking table structure: {str(e)}")
                return {
                    "status": "partial",
                    "message": f"Error checking table structure: {str(e)}",
                    "tables": [t[0] for t in tables]
                }
        except Exception as e:
            logger.error(f"Error listing tables: {str(e)}")
            return {
                "status": "partial",
                "message": f"Error listing tables: {str(e)}",
                "basic_query": result[0] == 1
            }
    except Exception as e:
        stack_trace = traceback.format_exc()
        logger.error(f"Database connection error: {str(e)}\n{stack_trace}")
        return {
            "status": "error",
            "message": f"Database connection error: {str(e)}",
            "stack_trace": stack_trace
        }

@router.post("/", status_code=200)
def create_rating(rating: RatingCreate, db: Session = Depends(get_db)):
    """Create a new rating for an activity"""
    try:
        logger.info(f"Creating rating for activity_key={rating.activity_key}, rating={rating.rating}")
        
        # Create new rating record with very minimal fields
        try:
            db_rating = Rating(
                activity_type=rating.activity_key,
                rating_value=rating.rating,
                user_id=None
            )
            
            db.add(db_rating)
            db.commit()
            db.refresh(db_rating)
            logger.info(f"Successfully saved rating ID={db_rating.id}")
        except Exception as e:
            stack_trace = traceback.format_exc()
            logger.error(f"Error creating rating record: {str(e)}\n{stack_trace}")
            raise HTTPException(status_code=500, detail=f"Error creating rating: {str(e)}")
        
        # Try to get updated stats for the activity
        try:
            stats = db.query(
                Rating.activity_type,
                func.count(Rating.id).label("count"),
                func.avg(Rating.rating_value).label("avg_rating")
            ).filter(Rating.activity_type == rating.activity_key).group_by(Rating.activity_type).first()
            
            if stats:
                logger.info(f"Retrieved stats: {stats}")
                count = stats.count
                avg_rating = float(stats.avg_rating)
            else:
                # No stats, use the current rating
                logger.info("No existing stats, using current rating")
                count = 1
                avg_rating = float(rating.rating)
        except Exception as e:
            stack_trace = traceback.format_exc()
            logger.error(f"Error retrieving stats: {str(e)}\n{stack_trace}")
            # Fallback to default values
            count = 1
            avg_rating = float(rating.rating)
        
        # Create response with CORS headers
        response_data = {
            "rating": {
                "id": db_rating.id,
                "activity_key": rating.activity_key,
                "rating": rating.rating
            },
            "stats": {
                "activity_key": rating.activity_key,
                "count": count,
                "average_rating": avg_rating,
                "total_ratings": count
            }
        }
        
        response = Response(
            content=json.dumps(response_data),
            media_type="application/json"
        )
        
        # Add CORS headers
        response.headers["Access-Control-Allow-Origin"] = "*"
        response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS"
        response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
        
        return response
    except Exception as e:
        stack_trace = traceback.format_exc()
        logger.error(f"Error while creating rating: {str(e)}\n{stack_trace}")
        raise HTTPException(status_code=500, detail=f"Error while creating rating: {str(e)}")

@router.put("/")
def update_rating(rating: RatingCreate, db: Session = Depends(get_db)):
    """Update an existing rating by creating a new one"""
    return create_rating(rating, db)

@router.post("/{id}")
def create_rating_with_id(id: str, rating: RatingCreate, db: Session = Depends(get_db)):
    """Create a rating with a specified ID (ID is ignored)"""
    return create_rating(rating, db)

@router.put("/{id}")
def update_rating_with_id(id: str, rating: RatingCreate, db: Session = Depends(get_db)):
    """Update a rating with a specified ID (ID is ignored)"""
    return create_rating(rating, db)

@router.get("/")
def get_all_stats():
    """Get statistics for all activities"""
    try:
        logger.info("Getting statistics for all activities")
        
        try:
            # Use direct session instead of generator
            db = get_db_session()
            try:
                stats = db.query(
                    Rating.activity_type,
                    func.count(Rating.id).label("count"),
                    func.avg(Rating.rating_value).label("avg_rating")
                ).group_by(Rating.activity_type).all()
                
                if stats:
                    logger.info(f"Retrieved stats for {len(stats)} activities")
                    results = []
                    for stat in stats:
                        results.append(ActivityStats(
                            activity_key=stat.activity_type,
                            count=stat.count,
                            average_rating=float(stat.avg_rating),
                            total_ratings=stat.count
                        ))
                    return results
                else:
                    logger.info("No ratings found in database")
                    return []
            finally:
                db.close()
        except Exception as e:
            stack_trace = traceback.format_exc()
            logger.error(f"Error querying statistics: {str(e)}\n{stack_trace}")
            return []
    except Exception as e:
        stack_trace = traceback.format_exc()
        logger.error(f"Error while getting all statistics: {str(e)}\n{stack_trace}")
        return []

@router.get("/{activity_key}", response_model=ActivityStats)
def get_activity_stats(activity_key: str):
    """Get statistics for a specific activity"""
    try:
        logger.info(f"Getting statistics for activity {activity_key}")
        
        try:
            # Use direct session instead of generator
            db = get_db_session()
            try:
                # Make sure to use db directly, not as a generator
                stat = db.query(
                    Rating.activity_type,
                    func.count(Rating.id).label("count"),
                    func.avg(Rating.rating_value).label("avg_rating")
                ).filter(Rating.activity_type == activity_key).group_by(Rating.activity_type).first()
                
                if stat:
                    logger.info(f"Retrieved stats: count={stat.count}, avg={stat.avg_rating}")
                    stats = ActivityStats(
                        activity_key=activity_key,
                        count=stat.count,
                        average_rating=float(stat.avg_rating),
                        total_ratings=stat.count
                    )
                else:
                    logger.info(f"No ratings found for activity {activity_key}")
                    stats = ActivityStats(
                        activity_key=activity_key,
                        count=0,
                        average_rating=0.0,
                        total_ratings=0
                    )
                
                # Convert to dict and return as JSON with CORS headers
                response_data = stats.dict()
                response = Response(
                    content=json.dumps(response_data),
                    media_type="application/json"
                )
                
                # Add CORS headers
                response.headers["Access-Control-Allow-Origin"] = "*"
                response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS"
                response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
                
                return response
            finally:
                db.close()
        except Exception as e:
            stack_trace = traceback.format_exc()
            logger.error(f"Query error in get_activity_stats for {activity_key}: {str(e)}\n{stack_trace}")
            # Return default stats instead of error
            stats = ActivityStats(
                activity_key=activity_key,
                count=0,
                average_rating=0.0,
                total_ratings=0
            )
            
            # Convert to dict and return as JSON with CORS headers
            response_data = stats.dict()
            response = Response(
                content=json.dumps(response_data),
                media_type="application/json"
            )
            
            # Add CORS headers
            response.headers["Access-Control-Allow-Origin"] = "*"
            response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS"
            response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
            
            return response
    except Exception as e:
        stack_trace = traceback.format_exc()
        logger.error(f"Error while getting statistics for activity {activity_key}: {str(e)}\n{stack_trace}")
        # Return default stats instead of error
        stats = ActivityStats(
            activity_key=activity_key,
            count=0,
            average_rating=0.0,
            total_ratings=0
        )
        
        # Convert to dict and return as JSON with CORS headers
        response_data = stats.dict()
        response = Response(
            content=json.dumps(response_data),
            media_type="application/json"
        )
        
        # Add CORS headers
        response.headers["Access-Control-Allow-Origin"] = "*"
        response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS"
        response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
        
        return response 