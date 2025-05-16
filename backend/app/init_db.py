from app.database import SessionLocal, create_tables, engine
from app.models.rating import Rating
from sqlalchemy.exc import IntegrityError
from sqlalchemy import inspect

def init_ratings():
    db = SessionLocal()
    try:
        # 检查表是否存在
        inspector = inspect(engine)
        if not inspector.has_table("activity_ratings"):
            print("Table 'activity_ratings' does not exist. Creating tables...")
            create_tables()
        
        # 创建一些初始评分数据
        initial_ratings = [
            # 为每个活动类型创建多条评分记录，模拟多人评分
            # breathing活动
            Rating(activity_key="breathing", rating=5),
            Rating(activity_key="breathing", rating=4),
            Rating(activity_key="breathing", rating=5),
            # meditation活动
            Rating(activity_key="meditation", rating=4),
            Rating(activity_key="meditation", rating=5),
            Rating(activity_key="meditation", rating=3),
            # grounding活动
            Rating(activity_key="grounding", rating=5),
            Rating(activity_key="grounding", rating=4),
            # nature活动
            Rating(activity_key="nature", rating=4),
            Rating(activity_key="nature", rating=5),
            # stretching活动
            Rating(activity_key="stretching", rating=5),
            Rating(activity_key="stretching", rating=4),
            # color-breathing活动
            Rating(activity_key="color-breathing", rating=4),
            Rating(activity_key="color-breathing", rating=3),
            # affirmation活动
            Rating(activity_key="affirmation", rating=5),
            Rating(activity_key="affirmation", rating=4),
        ]
        
        for rating in initial_ratings:
            db.add(rating)
            db.commit()
            print(f"Added rating for {rating.activity_key}: {rating.rating}")
    except Exception as e:
        db.rollback()
        print(f"Error: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    print("Initializing ratings data...")
    init_ratings()
    print("Database initialization complete!") 