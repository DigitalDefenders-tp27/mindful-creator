from fastapi import APIRouter, Depends, HTTPException, Path, Request
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Dict, Any
from app.database import get_db
from app.models.rating import Rating
from app.schemas.rating import RatingCreate, Rating as RatingSchema, ActivityStats

router = APIRouter()

@router.post("/")
def create_rating(rating: RatingCreate, db: Session = Depends(get_db)):
    # 总是创建新的评分记录
    db_rating = Rating(
        activity_key=rating.activity_key,
        rating=rating.rating
    )
    db.add(db_rating)
    db.commit()
    db.refresh(db_rating)
    
    # 获取该活动的更新统计信息
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

# Add PUT endpoint with the same functionality as POST
@router.put("/")
def update_rating(rating: RatingCreate, db: Session = Depends(get_db)):
    # Same implementation as create_rating to support both methods
    db_rating = Rating(
        activity_key=rating.activity_key,
        rating=rating.rating
    )
    db.add(db_rating)
    db.commit()
    db.refresh(db_rating)
    
    # 获取该活动的更新统计信息
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

@router.get("/", response_model=List[ActivityStats])
def get_all_stats(db: Session = Depends(get_db)):
    stats = db.query(
        Rating.activity_key,
        func.count(Rating.id).label("count"),
        func.avg(Rating.rating).label("average_rating"),
        func.count(Rating.id).label("total_ratings")
    ).group_by(
        Rating.activity_key
    ).all()

    return [
        ActivityStats(
            activity_key=stat[0],
            count=stat[1],
            average_rating=float(stat[2] or 0),
            total_ratings=stat[3]
        )
        for stat in stats
    ]

# 通配符路径 - 处理所有POST请求到/api/ratings/开头的任何路径
@router.post("/{path:path}")
async def create_rating_wildcard(path: str, request: Request, rating: RatingCreate, db: Session = Depends(get_db)):
    print(f"Rating POST received at wildcard path: /{path}")
    return create_rating(rating, db)

# 通配符路径 - 处理所有PUT请求到/api/ratings/开头的任何路径
@router.put("/{path:path}")
async def update_rating_wildcard(path: str, request: Request, rating: RatingCreate, db: Session = Depends(get_db)):
    print(f"Rating PUT received at wildcard path: /{path}")
    return update_rating(rating, db)

@router.get("/{activity_key}", response_model=ActivityStats)
def get_activity_stats(activity_key: str, db: Session = Depends(get_db)):
    # 首先检查这是否是一个特殊路径，如"/:1"
    if activity_key.startswith(":") or activity_key.startswith("="):
        # 如果是特殊路径，返回空数据而不是查询数据库
        return ActivityStats(
            activity_key="unknown",
            count=0,
            average_rating=0.0,
            total_ratings=0
        )
        
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
        return ActivityStats(
            activity_key=activity_key,
            count=0,
            average_rating=0.0,
            total_ratings=0
        )
    
    return ActivityStats(
        activity_key=stats[0],
        count=stats[1],
        average_rating=float(stats[2] or 0),
        total_ratings=stats[3]
    ) 