from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
import re
import logging
import time
from dotenv import load_dotenv
from tenacity import retry, wait_exponential, stop_after_attempt, retry_if_exception_type
from sqlalchemy.exc import OperationalError, DatabaseError

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("database")

load_dotenv()

# Get DATABASE_URL from environment variables, trying both common variables
# First try DATABASE_PUBLIC_URL (Railway-specific), then fall back to DATABASE_URL
raw_database_url = os.getenv("DATABASE_PUBLIC_URL") or os.getenv("DATABASE_URL", "sqlite:///./relaxation.db")

# Log which database URL we're using
if os.getenv("DATABASE_PUBLIC_URL"):
    logger.info("Using DATABASE_PUBLIC_URL environment variable")
elif os.getenv("DATABASE_URL"):
    logger.info("Using DATABASE_URL environment variable")
else:
    logger.warning("No database URL environment variables found, using default SQLite database")

# Handle Railway PostgreSQL URLs if provided
if raw_database_url and "postgres" in raw_database_url:
    # If it's just a hostname, convert it to a proper URL format
    if not raw_database_url.startswith("postgresql://"):
        # Default to a standard format if only the hostname is provided
        DATABASE_URL = f"postgresql://postgres:postgres@{raw_database_url}:5432/railway"
        logger.info("Converted hostname to full PostgreSQL URL")
    else:
        # If it's a full URL but potentially has the "postgres://" prefix (which SQLAlchemy doesn't support)
        DATABASE_URL = raw_database_url.replace("postgres://", "postgresql://")
        logger.info("Converted postgres:// to postgresql:// in URL")
    
    # Get the database connect timeout from environment or default to 30 seconds
    db_timeout = int(os.getenv("DATABASE_CONNECT_TIMEOUT", "30"))
    
    try:
        # Create database engine with PostgreSQL-specific pool settings and improved resilience
        logger.info(f"Creating PostgreSQL engine with {db_timeout}s timeout")
        engine = create_engine(
            DATABASE_URL,
            pool_size=5,
            max_overflow=10,
            pool_timeout=db_timeout,
            pool_recycle=300,  # Recycle connections after 5 minutes
            pool_pre_ping=True,  # Check connection before using from pool
            connect_args={
                "connect_timeout": db_timeout,
                "keepalives": 1,
                "keepalives_idle": 30,
                "keepalives_interval": 10,
                "keepalives_count": 5
            }
        )
        logger.info("PostgreSQL engine created successfully")
    except Exception as e:
        logger.error(f"Error creating PostgreSQL engine: {e}")
        # Fall back to SQLite if allowed
        if os.getenv("ALLOW_DB_FAILURE", "false").lower() == "true":
            logger.warning("Falling back to in-memory SQLite database due to PostgreSQL connection error")
            DATABASE_URL = "sqlite:///:memory:"
            engine = create_engine(DATABASE_URL)
        else:
            raise
else:
    # SQLite doesn't support pooling parameters
    DATABASE_URL = raw_database_url
    logger.info(f"Using SQLite database: {DATABASE_URL}")
    engine = create_engine(DATABASE_URL)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create base class
Base = declarative_base()

# Dependency with retry logic
@retry(
    retry=retry_if_exception_type((OperationalError, DatabaseError)),
    wait=wait_exponential(multiplier=1, min=1, max=10),
    stop=stop_after_attempt(3)
)
def get_db():
    """
    Get database session with retry logic for transient connection issues
    """
    db = SessionLocal()
    try:
        # Test the connection with a simple query
        db.execute("SELECT 1")
        yield db
    except Exception as e:
        logger.error(f"Database connection error: {e}")
        raise
    finally:
        db.close()

# Create tables safely
def create_tables():
    """Create all tables defined in models"""
    try:
        logger.info("Creating database tables")
        Base.metadata.create_all(bind=engine)
        logger.info("Database tables created successfully")
    except Exception as e:
        logger.error(f"Error creating tables: {e}")
        if os.getenv("ALLOW_DB_FAILURE", "false").lower() != "true":
            raise

if __name__ == "__main__":
    create_tables()
    print("Database tables created successfully!")

# Import for backwards compatibility
try:
    from backend.database import get_connection
except ImportError:
    # Fallback implementation if needed
    def get_connection():
        """Fallback implementation of get_connection"""
        logger.warning("Using fallback get_connection implementation")
        return engine.connect()
