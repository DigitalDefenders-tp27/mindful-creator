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

# OPTIONS方法支持预检请求
@router.options("/{path:path}")
async def options_ratings_all_paths():
    return Response(status_code=200)

@router.post("/")
def create_rating(rating: RatingCreate, db: Session = Depends(get_db)):
    try:
        logger.info(f"接收到新评分: activity_key={rating.activity_key}, rating={rating.rating}")
        
        # 创建新的评分记录
        db_rating = Rating(
            activity_key=rating.activity_key,
            rating=rating.rating
        )
        db.add(db_rating)
        db.commit()
        db.refresh(db_rating)
        logger.info(f"成功保存评分 ID={db_rating.id}")
        
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
            logger.warning(f"未找到活动 {rating.activity_key} 的统计信息，这应该是这个活动的第一个评分")
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
        
        logger.info(f"活动 {rating.activity_key} 的统计信息: count={stats[1]}, avg={stats[2]}, total={stats[3]}")
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
        logger.error(f"创建评分时出错: {str(e)}")
        raise HTTPException(status_code=500, detail=f"创建评分时出错: {str(e)}")

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
        logger.info("获取所有活动的统计信息")
        stats = db.query(
            Rating.activity_key,
            func.count(Rating.id).label("count"),
            func.avg(Rating.rating).label("average_rating"),
            func.count(Rating.id).label("total_ratings")
        ).group_by(
            Rating.activity_key
        ).all()
        
        logger.info(f"找到 {len(stats)} 个活动的统计信息")
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
        logger.error(f"获取所有统计信息时出错: {str(e)}")
        raise HTTPException(status_code=500, detail=f"获取统计信息时出错: {str(e)}")

@router.get("/{activity_key}", response_model=ActivityStats)
def get_activity_stats(activity_key: str, db: Session = Depends(get_db)):
    try:
        logger.info(f"获取活动 {activity_key} 的统计信息")
        
        # 特殊路径处理
        if activity_key.startswith(":") or activity_key == "1":
            logger.info(f"检测到特殊路径 {activity_key}，返回默认空统计")
            return ActivityStats(
                activity_key="default",
                count=0,
                average_rating=0.0,
                total_ratings=0
            )
            
        # 查询数据库
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
            logger.info(f"未找到活动 {activity_key} 的统计信息")
            return ActivityStats(
                activity_key=activity_key,
                count=0,
                average_rating=0.0,
                total_ratings=0
            )
        
        logger.info(f"找到活动 {activity_key} 的统计信息: count={stats[1]}, avg={stats[2]}, total={stats[3]}")
        return ActivityStats(
            activity_key=stats[0],
            count=stats[1],
            average_rating=float(stats[2] or 0),
            total_ratings=stats[3]
        )
    except Exception as e:
        logger.error(f"获取活动 {activity_key} 的统计信息时出错: {str(e)}")
        raise HTTPException(status_code=500, detail=f"获取统计信息时出错: {str(e)}") 