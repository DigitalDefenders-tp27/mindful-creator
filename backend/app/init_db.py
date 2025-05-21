from app.database import SessionLocal, create_tables, engine
from app.models.rating import Rating
from sqlalchemy.exc import IntegrityError
from sqlalchemy import inspect

def init_ratings():
    db = SessionLocal()
    try:
        # Check if the table exists
        inspector = inspect(engine)
        if not inspector.has_table("activity_ratings"):
            print("Table 'activity_ratings' does not exist. Creating tables...")
            create_tables()
        
        # Create initial rating data
        initial_ratings = [
            # Create multiple rating records for each activity type to simulate user ratings
            # Breathing activity
            Rating(activity_key="breathing", rating=5),
            Rating(activity_key="breathing", rating=4),
            Rating(activity_key="breathing", rating=5),
            # Meditation activity
            Rating(activity_key="meditation", rating=4),
            Rating(activity_key="meditation", rating=5),
            Rating(activity_key="meditation", rating=3),
            # Grounding activity
            Rating(activity_key="grounding", rating=5),
            Rating(activity_key="grounding", rating=4),
            # Nature activity
            Rating(activity_key="nature", rating=4),
            Rating(activity_key="nature", rating=5),
            # Stretching activity
            Rating(activity_key="stretching", rating=5),
            Rating(activity_key="stretching", rating=4),
            # Colour breathing activity
            Rating(activity_key="color-breathing", rating=4),
            Rating(activity_key="color-breathing", rating=3),
            # Affirmation activity
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
    print("Initialising ratings data...")
    init_ratings()
    print("Database initialisation complete!") 