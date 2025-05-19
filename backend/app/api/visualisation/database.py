import os
import logging
import traceback
import sys
import json
import time
import threading
from sqlalchemy import create_engine, text, Column, Integer, String, Float, MetaData, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, load_only
from sqlalchemy.ext.automap import automap_base
from dotenv import load_dotenv
from contextlib import contextmanager

load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("visualisation.database")

# Get DATABASE_URL from environment variables
DATABASE_URL = os.getenv("DATABASE_PUBLIC_URL") or os.getenv("DATABASE_URL", "postgresql://postgres:postgres@postgres-production-7575.up.railway.app:5432/railway")

# Log which environment variable was used
if os.getenv("DATABASE_PUBLIC_URL"):
    logger.info("Using DATABASE_PUBLIC_URL environment variable")
elif os.getenv("DATABASE_URL"):
    logger.info("Using DATABASE_URL environment variable")
else:
    logger.warning("No database URL environment variable found, using default")

# Check for environment variables that affect database handling
ALLOW_DB_FAILURE = os.getenv("ALLOW_DB_FAILURE", "false").lower() == "true"
DATABASE_CONNECT_TIMEOUT = int(os.getenv("DATABASE_CONNECT_TIMEOUT", "30"))

logger.info(f"ALLOW_DB_FAILURE: {ALLOW_DB_FAILURE}")
logger.info(f"DATABASE_CONNECT_TIMEOUT: {DATABASE_CONNECT_TIMEOUT}")

# Handle Railway PostgreSQL URLs
if "postgres://" in DATABASE_URL:
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://")

# Check if this is a Railway PostgreSQL URL
is_railway_db = "railway.app" in DATABASE_URL

# Log connection environment
if is_railway_db:
    logger.info("Detected Railway PostgreSQL database")

# Mask the password for logging
def get_masked_url(url):
    if '@' not in url:
        return "unknown"
    parts = url.split('@')
    auth_parts = parts[0].split('://')
    if len(auth_parts) < 2:
        return f"unknown@{parts[1]}"
    protocol = auth_parts[0]
    auth = auth_parts[1].split(':')
    user = auth[0] if len(auth) > 0 else "unknown"
    return f"{protocol}://{user}:****@{parts[1]}"

logger.info(f"Connecting to database at: {get_masked_url(DATABASE_URL)}")

# Timeout wrapper for database operations
class TimeoutError(Exception):
    pass

def timeout_handler():
    raise TimeoutError("Database operation timed out")

@contextmanager
def time_limit(seconds):
    """Context manager to add timeout to a database operation"""
    timer = threading.Timer(seconds, timeout_handler)
    timer.start()
    try:
        yield
    finally:
        timer.cancel()

# Database connection engine and session factory
try:
    logger.info(f"Attempting to create database engine with timeout {DATABASE_CONNECT_TIMEOUT}s")
    # Create database engine with PostgreSQL-specific settings and increased timeouts
    engine = create_engine(
        DATABASE_URL,
        pool_size=5,               # Increased from 3 to 5
        max_overflow=10,           # Increased from 5 to 10
        pool_timeout=DATABASE_CONNECT_TIMEOUT,  # Use env var
        pool_recycle=300,          # Recycle connections after 5 minutes
        pool_pre_ping=True,        # Send a ping before using a connection
        connect_args={
            "connect_timeout": DATABASE_CONNECT_TIMEOUT,  # Use env var
            "keepalives": 1,       # Enable TCP keepalive
            "keepalives_idle": 30, # Idle time before sending keepalives
            "keepalives_interval": 10, # Interval between keepalives
            "keepalives_count": 5, # Number of keepalives before giving up
            "options": f"-c statement_timeout={DATABASE_CONNECT_TIMEOUT * 1000}"  # Use env var
        }
    )
    
    # Create session factory
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    
    # Create base classes for ORM
    Base = declarative_base()
    AutomapBase = automap_base()
    
    # Reflect the database structure
    logger.info("Attempting to reflect database structure")
    
    # Create empty objects first in case reflection fails
    TrainCleaned = None
    SmmhCleaned = None
    TrainCleanedModel = None
    SmmhCleanedModel = None
    
    try:
        metadata = MetaData()
        metadata.reflect(bind=engine)
        
        # Define ORM models for required tables
        if 'train_cleaned' in metadata.tables:
            TrainCleaned = Table('train_cleaned', metadata, autoload_with=engine)
        
        if 'smmh_cleaned' in metadata.tables:
            SmmhCleaned = Table('smmh_cleaned', metadata, autoload_with=engine)
        
        # Auto-map existing tables to ORM models
        AutomapBase.prepare(engine, reflect=True)
        
        # Try to get the models from the automap if they exist
        try:
            TrainCleanedModel = AutomapBase.classes.train_cleaned if hasattr(AutomapBase.classes, 'train_cleaned') else None
            SmmhCleanedModel = AutomapBase.classes.smmh_cleaned if hasattr(AutomapBase.classes, 'smmh_cleaned') else None
            logger.info(f"ORM Models loaded: TrainCleaned={TrainCleanedModel is not None}, SmmhCleaned={SmmhCleanedModel is not None}")
        except Exception as e:
            logger.error(f"Error loading ORM models: {e}")
            TrainCleanedModel = None
            SmmhCleanedModel = None
    
        logger.info("Database engine and ORM models created successfully")
    except Exception as e:
        logger.error(f"Error reflecting database structure: {e}")
        if not ALLOW_DB_FAILURE:
            raise
        logger.warning("Continuing despite database reflection failure (ALLOW_DB_FAILURE=true)")
        
except Exception as e:
    logger.error(f"Error setting up database: {e}")
    logger.error(traceback.format_exc())
    if not ALLOW_DB_FAILURE:
        raise
    logger.warning("Continuing despite database setup failure (ALLOW_DB_FAILURE=true)")
    
    # Create dummy engine and session for the app to start
    # These won't work but will allow the app to initialize
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker
    
    engine = create_engine("sqlite:///:memory:")
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    TrainCleaned = None
    SmmhCleaned = None
    TrainCleanedModel = None
    SmmhCleanedModel = None

def log_connection_details(operation="general", status="attempted", details=None):
    """
    Log detailed connection information to help debug deployment issues
    
    Args:
        operation: String describing the operation being performed
        status: Status of the operation (attempted, success, failed)
        details: Any additional details or error information
    """
    try:
        # Get system environment details
        sys_info = {
            "python_version": sys.version,
            "platform": sys.platform,
            "environment": os.environ.get("ENVIRONMENT", "unknown"),
            "server_time": time.strftime('%Y-%m-%d %H:%M:%S'),
        }
        
        # Database connection details (with sensitive info masked)
        db_info = {
            "database_url": get_masked_url(DATABASE_URL),
            "operation": operation,
            "status": status,
        }
        
        # Add any additional details
        if details:
            db_info["details"] = details
            
        # Create log message
        log_message = f"DATABASE CONNECTION LOG | Operation: {operation} | Status: {status}"
        
        # Add full context as JSON
        context = {"system": sys_info, "database": db_info}
        
        # Log appropriately based on status
        if status == "failed":
            logger.error(f"{log_message}\nContext: {json.dumps(context, indent=2)}")
        else:
            logger.info(f"{log_message}\nContext: {json.dumps(context, indent=2)}")
    
    except Exception as e:
        # Ensure logging itself doesn't cause issues
        logger.error(f"Error in logging function: {e}")

def get_db():
    """Database session dependency"""
    log_connection_details("session_start", "attempted")
    db = SessionLocal()
    try:
        yield db
        log_connection_details("session_end", "success")
    except Exception as e:
        log_connection_details("session_error", "failed", str(e))
        raise
    finally:
        db.close()

def execute_query(query_str, params=None, timeout=30, max_retries=2):
    """
    Execute a raw SQL query and return the results as a list of dictionaries
    With a configurable timeout (default 30 seconds) and retry mechanism
    """
    operation = "execute_query"
    start_time = time.time()
    
    # Log the query being attempted (truncate if too long)
    truncated_query = query_str[:500] + "..." if len(query_str) > 500 else query_str
    log_connection_details(operation, "attempted", {"query": truncated_query, "timeout": timeout})
    
    last_error = None
    for retry in range(max_retries + 1):  # +1 because first attempt is not a retry
        if retry > 0:
            logger.info(f"Retry {retry}/{max_retries} for database query after {retry * 2} seconds delay")
            time.sleep(retry * 2)  # Progressive backoff
        
        try:
            # Use timeout context manager to ensure query doesn't hang
            with time_limit(timeout):
                with engine.connect() as connection:
                    # Set statement timeout at connection level as well
                    connection.execute(text(f"SET statement_timeout = {timeout * 1000}"))
                    
                    # Execute the query
                    result = connection.execute(text(query_str), params or {})
                    columns = result.keys()
                    rows = result.fetchall()
                    duration = time.time() - start_time
                    
                    # Log successful query execution
                    row_count = len(rows)
                    log_connection_details(operation, "success", {
                        "rows_returned": row_count,
                        "duration_ms": round(duration * 1000, 2),
                        "query_truncated": truncated_query,
                        "retries": retry
                    })
                    
                    return [dict(zip(columns, row)) for row in rows]
        except TimeoutError as e:
            last_error = e
            duration = time.time() - start_time
            error_details = {
                "error_type": "TimeoutError",
                "error_msg": f"Query execution timed out after {timeout} seconds",
                "duration_ms": round(duration * 1000, 2),
                "query_truncated": truncated_query,
                "retry": retry,
                "max_retries": max_retries
            }
            log_connection_details(operation, "timeout", error_details)
            logger.error(f"Query timed out after {timeout} seconds (retry {retry}/{max_retries}): {truncated_query}")
            
            # If this is the last retry, raise the error
            if retry == max_retries:
                raise TimeoutError(f"Database query timed out after {timeout} seconds and {max_retries} retries")
        except Exception as e:
            # Log the failure with detailed error info
            last_error = e
            duration = time.time() - start_time
            error_details = {
                "error_type": type(e).__name__,
                "error_msg": str(e),
                "duration_ms": round(duration * 1000, 2),
                "query_truncated": truncated_query,
                "retry": retry,
                "max_retries": max_retries,
                "traceback": traceback.format_exc()
            }
            log_connection_details(operation, "failed", error_details)
            logger.error(f"Error executing query (retry {retry}/{max_retries}): {e}")
            
            # If this is the last retry, raise the error
            if retry == max_retries:
                raise
    
    # This should not be reached, but just in case
    raise last_error or Exception("Unknown database error")

# Get data using the SQLAlchemy ORM
def get_train_cleaned_data(filters=None, group_by=None):
    """
    Use ORM to query the train_cleaned table with the given filters
    
    Args:
        filters: Dictionary of column:value pairs to filter on
        group_by: List of columns to group by
    
    Returns:
        List of dictionaries with the query results
    """
    if TrainCleaned is None:
        logger.error("TrainCleaned table not found in database schema")
        raise Exception("Train cleaned table not available")
    
    operation = "get_train_cleaned_data"
    log_connection_details(operation, "attempted")
    
    try:
        with time_limit(30):
            with engine.connect() as conn:
                # Build a select query using the ORM Table
                query = TrainCleaned.select()
                
                # Apply filters if provided
                if filters:
                    for column, value in filters.items():
                        if isinstance(value, list):
                            query = query.where(getattr(TrainCleaned.c, column).in_(value))
                        else:
                            query = query.where(getattr(TrainCleaned.c, column) == value)
                
                # Execute the query
                result = conn.execute(query)
                rows = result.fetchall()
                
                # Convert to dictionaries
                data = [dict(row) for row in rows]
                
                log_connection_details(operation, "success", {"rows_returned": len(data)})
                return data
    except Exception as e:
        log_connection_details(operation, "failed", {"error": str(e)})
        logger.error(f"Error in get_train_cleaned_data: {e}")
        raise

def get_smmh_cleaned_data(filters=None, group_by=None):
    """
    Use ORM to query the smmh_cleaned table with the given filters
    
    Args:
        filters: Dictionary of column:value pairs to filter on
        group_by: List of columns to group by
    
    Returns:
        List of dictionaries with the query results
    """
    if SmmhCleaned is None:
        logger.error("SmmhCleaned table not found in database schema")
        raise Exception("SMMH cleaned table not available")
    
    operation = "get_smmh_cleaned_data"
    log_connection_details(operation, "attempted")
    
    try:
        with time_limit(30):
            with engine.connect() as conn:
                # Build a select query using the ORM Table
                query = SmmhCleaned.select()
                
                # Apply filters if provided
                if filters:
                    for column, value in filters.items():
                        if isinstance(value, list):
                            query = query.where(getattr(SmmhCleaned.c, column).in_(value))
                        else:
                            query = query.where(getattr(SmmhCleaned.c, column) == value)
                
                # Execute the query
                result = conn.execute(query)
                rows = result.fetchall()
                
                # Convert to dictionaries
                data = [dict(row) for row in rows]
                
                log_connection_details(operation, "success", {"rows_returned": len(data)})
                return data
    except Exception as e:
        log_connection_details(operation, "failed", {"error": str(e)})
        logger.error(f"Error in get_smmh_cleaned_data: {e}")
        raise 