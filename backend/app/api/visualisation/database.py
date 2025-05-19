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

# Configure logging - Use a unique name for this logger
logger = logging.getLogger("mindful-creator.visualisation.database")
# Ensure handlers are set up if not configured globally (e.g. by main.py)
if not logger.handlers:
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    logger.info("Configured basicConfig for visualisation.database logger.")

# Get DATABASE_URL from environment variables
DATABASE_URL = os.getenv("DATABASE_PUBLIC_URL") or os.getenv("DATABASE_URL")
FALLBACK_DB_URL = "sqlite:///:memory:" # In-memory SQLite as a last resort

# Log which environment variable was used
if os.getenv("DATABASE_PUBLIC_URL"):
    logger.info("Using DATABASE_PUBLIC_URL environment variable for visualisation database.")
elif os.getenv("DATABASE_URL"):
    logger.info("Using DATABASE_URL environment variable for visualisation database.")
else:
    logger.warning("No primary database URL (DATABASE_PUBLIC_URL or DATABASE_URL) found for visualisation. Will attempt fallback if ALLOW_DB_FAILURE is true.")

# Check for environment variables that affect database handling
ALLOW_DB_FAILURE = os.getenv("ALLOW_DB_FAILURE", "false").lower() == "true"
DATABASE_CONNECT_TIMEOUT = int(os.getenv("DATABASE_CONNECT_TIMEOUT", "30"))

logger.info(f"Visualisation DB - ALLOW_DB_FAILURE: {ALLOW_DB_FAILURE}")
logger.info(f"Visualisation DB - DATABASE_CONNECT_TIMEOUT: {DATABASE_CONNECT_TIMEOUT}")

# Handle Railway PostgreSQL URLs
if DATABASE_URL and "postgres://" in DATABASE_URL:
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://")
    logger.info("Visualisation DB - Converted postgres:// to postgresql://")

# Check if this is a Railway PostgreSQL URL
is_railway_db = "railway.app" in DATABASE_URL

# Log connection environment
if is_railway_db:
    logger.info("Detected Railway PostgreSQL database")

# Mask the password for logging
def get_masked_url(url):
    if not url or '@' not in url:
        return str(url) # Return as is if None or no auth part
    parts = url.split('@')
    auth_parts = parts[0].split('://')
    if len(auth_parts) < 2:
        return f"unknown@{parts[1]}"
    protocol = auth_parts[0]
    auth = auth_parts[1].split(':')
    user = auth[0] if len(auth) > 0 else "unknown"
    return f"{protocol}://{user}:****@{parts[1]}"

logger.info(f"Visualisation DB - Effective DATABASE_URL: {get_masked_url(DATABASE_URL)}")

# Timeout wrapper for database operations
class TimeoutError(Exception):
    pass

def timeout_handler():
    raise TimeoutError("Database operation timed out in visualisation.database")

@contextmanager
def time_limit(seconds):
    timer = threading.Timer(seconds, timeout_handler)
    timer.start()
    try:
        yield
    finally:
        timer.cancel()

# Initialize globals that will be set in try_initialize_database
engine = None
SessionLocal = None
Base = declarative_base()
AutomapBase = automap_base()
TrainCleaned = None
SmmhCleaned = None
TrainCleanedModel = None
SmmhCleanedModel = None

def try_initialize_database():
    global engine, SessionLocal, Base, AutomapBase, TrainCleaned, SmmhCleaned, TrainCleanedModel, SmmhCleanedModel
    
    db_url_to_use = DATABASE_URL

    if not db_url_to_use:
        if ALLOW_DB_FAILURE:
            logger.warning("Visualisation DB - No DATABASE_URL set, and ALLOW_DB_FAILURE is true. Using fallback SQLite DB.")
            db_url_to_use = FALLBACK_DB_URL
        else:
            logger.critical("Visualisation DB - No DATABASE_URL set, and ALLOW_DB_FAILURE is false. Cannot initialize database.")
            # Potentially raise an error here or let parts of the app fail if they try to use it
            return False # Indicate failure

    try:
        logger.info(f"Visualisation DB - Attempting to create engine with URL: {get_masked_url(db_url_to_use)} and timeout {DATABASE_CONNECT_TIMEOUT}s")
        current_engine_args = {
            "pool_size": 5,
            "max_overflow": 10,
            "pool_timeout": DATABASE_CONNECT_TIMEOUT,
            "pool_recycle": 300,
            "pool_pre_ping": True,
            "connect_args": {
                "connect_timeout": DATABASE_CONNECT_TIMEOUT,
                "keepalives": 1,
                "keepalives_idle": 30,
                "keepalives_interval": 10,
                "keepalives_count": 5,
                "options": f"-c statement_timeout={DATABASE_CONNECT_TIMEOUT * 1000}"
            }
        }
        # SQLite does not support many of these args
        if "sqlite" in db_url_to_use:
            current_engine_args = {}

        engine = create_engine(db_url_to_use, **current_engine_args)
        logger.info("Visualisation DB - Engine created.")

        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        logger.info("Visualisation DB - SessionLocal created.")
        
        # Reflect the database structure only if not using fallback SQLite (unless explicitly needed)
        if "sqlite" not in db_url_to_use or db_url_to_use != FALLBACK_DB_URL:
            logger.info("Visualisation DB - Attempting to reflect database structure...")
            metadata = MetaData()
            try:
                metadata.reflect(bind=engine, views=True) # Include views if any
                logger.info(f"Visualisation DB - Reflection complete. Tables found: {list(metadata.tables.keys())}")

                if 'train_cleaned' in metadata.tables:
                    TrainCleaned = Table('train_cleaned', metadata, autoload_with=engine)
                    logger.info("Visualisation DB - TrainCleaned Table object created.")
                else:
                    logger.warning("Visualisation DB - 'train_cleaned' table not found in reflected metadata.")
                
                if 'smmh_cleaned' in metadata.tables:
                    SmmhCleaned = Table('smmh_cleaned', metadata, autoload_with=engine)
                    logger.info("Visualisation DB - SmmhCleaned Table object created.")
                    sys.stdout.flush() # Ensure this critical log gets out
                else:
                    logger.warning("Visualisation DB - 'smmh_cleaned' table not found in reflected metadata.")
                    sys.stdout.flush()

                logger.info("Visualisation DB - Checkpoint Gamma before AutomapBase logging.") # New checkpoint
                sys.stdout.flush() # Ensure checkpoint log gets out

                # Automap for ORM models
                logger.info("Visualisation DB - About to call AutomapBase.prepare()...")
                sys.stdout.flush() # Ensure this log gets out
                AutomapBase.prepare(engine, reflect=True, only=['train_cleaned', 'smmh_cleaned'])
                logger.info("Visualisation DB - AutomapBase.prepare() call completed.")
                sys.stdout.flush() # Ensure this log gets out

                TrainCleanedModel = AutomapBase.classes.train_cleaned if hasattr(AutomapBase.classes, 'train_cleaned') else None
                SmmhCleanedModel = AutomapBase.classes.smmh_cleaned if hasattr(AutomapBase.classes, 'smmh_cleaned') else None
                logger.info(f"Visualisation DB - ORM Models loaded via Automap: TrainCleanedModel={'Exists' if TrainCleanedModel else 'Not Found'}, SmmhCleanedModel={'Exists' if SmmhCleanedModel else 'Not Found'}")
            except Exception as reflect_error:
                logger.error(f"Visualisation DB - Error during ORM Automap or Table creation: {reflect_error}", exc_info=True)
                sys.stdout.flush() # Ensure error log gets out
                if not ALLOW_DB_FAILURE:
                    logger.critical("Visualisation DB - Raising reflection error as ALLOW_DB_FAILURE is false.")
                    raise
                logger.warning("Visualisation DB - Continuing despite database reflection failure (ALLOW_DB_FAILURE=true). ORM features may be unavailable.")
        else:
            logger.info("Visualisation DB - Using SQLite fallback, skipping detailed reflection for now.")

        logger.info("Visualisation DB - Database initialization attempt complete.")
        return True # Indicate success

    except Exception as e:
        logger.critical(f"Visualisation DB - Error setting up database engine/session: {e}", exc_info=True)
        if not ALLOW_DB_FAILURE:
            logger.critical("Visualisation DB - Raising setup error as ALLOW_DB_FAILURE is false.")
            raise
        # If ALLOW_DB_FAILURE is true, try to set up a minimal fallback SQLite engine
        logger.warning("Visualisation DB - Attempting to set up fallback SQLite due to main DB setup failure (ALLOW_DB_FAILURE=true).")
        try:
            engine = create_engine(FALLBACK_DB_URL)
            SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
            logger.info("Visualisation DB - Fallback SQLite engine and SessionLocal created.")
            return True # Indicate partial success (fallback)
        except Exception as fallback_e:
            logger.critical(f"Visualisation DB - CRITICAL: Failed to set up even fallback SQLite engine: {fallback_e}", exc_info=True)
            # At this point, the app might be in a very broken state for this module.
            return False # Indicate total failure

# Attempt to initialize the database when the module is imported
INITIALIZATION_SUCCESSFUL = try_initialize_database()
if not INITIALIZATION_SUCCESSFUL:
    logger.error("VISUALISATION DATABASE FAILED TO INITIALIZE PROPERLY. Functionality may be degraded or unavailable.")

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
    if not SessionLocal:
        logger.error("Visualisation DB - SessionLocal not initialized. Cannot get DB session.")
        if ALLOW_DB_FAILURE and try_initialize_database(): # Attempt re-init
             logger.info("Visualisation DB - Re-initialization attempt made for get_db.")
        else:
            raise Exception("Database not initialized for visualisation module.")
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
    if not engine:
        logger.error("Visualisation DB - Engine not initialized. Cannot execute query.")
        if ALLOW_DB_FAILURE and try_initialize_database():
            logger.info("Visualisation DB - Re-initialization attempt made for execute_query.")
        else:
            raise Exception("Database engine not initialized for visualisation module.")
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
        logger.error("Visualisation DB - TrainCleaned ORM Table not available.")
        if ALLOW_DB_FAILURE:
            logger.warning("Visualisation DB - TrainCleaned not available, returning empty list due to ALLOW_DB_FAILURE.")
            return [] # Or raise a custom, non-blocking error
        raise Exception("TrainCleaned ORM Table not available in visualisation database.")
    
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
        logger.error(f"Error in get_train_cleaned_data: {e}", exc_info=True)
        if ALLOW_DB_FAILURE:
            return []
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
        logger.error("Visualisation DB - SmmhCleaned ORM Table not available.")
        if ALLOW_DB_FAILURE:
            logger.warning("Visualisation DB - SmmhCleaned not available, returning empty list due to ALLOW_DB_FAILURE.")
            return [] # Or raise a custom, non-blocking error
        raise Exception("SmmhCleaned ORM Table not available in visualisation database.")
    
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
        logger.error(f"Error in get_smmh_cleaned_data: {e}", exc_info=True)
        if ALLOW_DB_FAILURE:
            return []
        raise 