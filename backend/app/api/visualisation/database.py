import os
import logging
import traceback
import sys
import json
import time
import threading
from sqlalchemy import create_engine, text, Column, Integer, String, Float, MetaData, Table, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, load_only
from dotenv import load_dotenv
from contextlib import contextmanager
from sqlalchemy import inspect as sqlalchemy_inspect
from sqlalchemy.orm.properties import ColumnProperty

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
is_railway_db = False
if DATABASE_URL: # Add check to prevent error if DATABASE_URL is None
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
Base = declarative_base() # Standard declarative base

# Define ORM Models Explicitly
class TrainCleaned(Base):
    __tablename__ = 'train_cleaned'
    # Assuming 'User_ID' is the primary key as it's often an identifier.
    # If not, this should be changed to the actual primary key or a suitable candidate.
    user_id = Column("User_ID", Integer, primary_key=True, index=True)
    age = Column("Age", Text)
    gender = Column("Gender", String) # Using String, assuming it's not excessively long. Use Text for longer strings.
    platform = Column("Platform", String)
    daily_usage_time = Column("daily_usage_time", Float)
    posts_per_day = Column("posts_per_day", Float)
    likes_received_per_day = Column("likes_received_per_day", Float)
    comments_received_per_day = Column("comments_received_per_day", Float)
    messages_sent_per_day = Column("messages_sent_per_day", Float)
    dominant_emotion = Column("dominant_emotion", String)

class SmmhCleaned(Base):
    __tablename__ = 'smmh_cleaned'
    # smmh_id removed as it does not exist in the actual database table.
    # SQLAlchemy might have limitations with tables without an explicit PK in the model,
    # but for SELECTs it might work. If issues arise, we might need to designate
    # an existing column (e.g., timestamp_val) as primary_key=True in the ORM model.
    
    timestamp_val = Column("Timestamp", Text, primary_key=True) # DB: Timestamp (text) - Marked as PK for ORM
    q1_age = Column(Float)      # DB: q1_age (float8)
    q2_gender = Column(Text)    # DB: q2_gender (text)
    q3_relationship_status = Column(Text) # DB: q3_relationship_status (text)
    q4_occupation_status = Column(Text) # DB: q4_occupation_status (text)
    q5_org_affiliation = Column(Text)   # DB: q5_org_affiliation (text)
    q6_use_social_media = Column(Text)  # DB: q6_use_social_media (text)
    q7_platforms = Column(Text)         # DB: q7_platforms (text)
    q8_avg_sm_time = Column(Text)       # DB: q8_avg_sm_time (text)
    q9_unintentional_use = Column(Integer) # DB: q9_unintentional_use (int8)
    q10_distracted_by_sm = Column(Integer) # DB: q10_distracted_by_sm (int8)
    q11_restless_no_sm = Column(Integer)   # DB: q11_restless_no_sm (int8)
    q12_easily_distracted_scale = Column(Integer) # DB: q12_easily_distracted_scale (int8)
    q13_bothered_by_worries_scale = Column(Integer) # DB: q13_bothered_by_worries_scale (int8)
    q14_difficulty_concentrating_scale = Column(Integer) # DB: q14_difficulty_concentrating_scale (int8)
    q15_compare_to_others_scale = Column(Integer) # DB: q15_compare_to_others_scale (int8)
    q16_feel_about_comparisons = Column(Integer) # DB: q16_feel_about_comparisons (int8)
    q17_seek_validation_scale = Column(Integer) # DB: q17_seek_validation_scale (int8)
    q18_feel_depressed_scale = Column(Integer) # DB: q18_feel_depressed_scale (int8)
    q19_interest_fluctuation_scale = Column(Integer) # DB: q19_interest_fluctuation_scale (int8)
    q20_sleep_issues_scale = Column(Integer) # DB: q20_sleep_issues_scale (int8)
    
    usage_time_group = Column("Usage_Time_Group", Text) # Kept as per image, maps to DB "Usage_Time_Group"


def try_initialize_database():
    global engine, SessionLocal # Base, TrainCleaned, SmmhCleaned are defined at module level
    
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
                "options": f"-c statement_timeout={DATABASE_CONNECT_TIMEOUT * 1000}" # Statement timeout in ms
            }
        }
        # SQLite does not support many of these args
        if "sqlite" in db_url_to_use:
            current_engine_args = {}

        engine = create_engine(db_url_to_use, **current_engine_args)
        logger.info("Visualisation DB - Engine created.")
        sys.stdout.flush() # Ensure log is flushed

        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        logger.info("Visualisation DB - SessionLocal created.")
        sys.stdout.flush() # Ensure log is flushed
        
        # With declarative models defined above, we don't need to reflect or create Table objects here.
        # The ORM models (TrainCleaned, SmmhCleaned) are now defined classes.
        # If you needed to create these tables in the DB (e.g., for a new setup),
        # you would call Base.metadata.create_all(engine) typically in a migration script or main app setup.
        # For an existing DB, these definitions just map to them.
        logger.info("Visualisation DB - Declarative models TrainCleaned and SmmhCleaned are defined.")
        logger.info("Visualisation DB - Database initialization attempt complete (using declarative models).")
        sys.stdout.flush() # Ensure log is flushed
        return True # Indicate success

    except Exception as e:
        logger.critical(f"Visualisation DB - Error setting up database engine/session: {e}", exc_info=True)
        sys.stdout.flush() # Ensure error log is flushed
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
    """
    try:
        sys_info = {
            "python_version": sys.version,
            "platform": sys.platform,
            "environment": os.environ.get("ENVIRONMENT", "unknown"),
            "server_time": time.strftime('%Y-%m-%d %H:%M:%S'),
        }
        db_info = {
            "database_url": get_masked_url(DATABASE_URL),
            "operation": operation,
            "status": status,
        }
        if details:
            db_info["details"] = details
        log_message = f"DATABASE CONNECTION LOG | Operation: {operation} | Status: {status}"
        context = {"system": sys_info, "database": db_info}
        if status == "failed":
            logger.error(f"{log_message}\nContext: {json.dumps(context, indent=2)}")
        else:
            logger.info(f"{log_message}\nContext: {json.dumps(context, indent=2)}")
    except Exception as e:
        logger.error(f"Error in logging function: {e}")

@contextmanager
def get_db():
    """Database session dependency"""
    if not SessionLocal:
        logger.error("Visualisation DB - SessionLocal not initialized. Cannot get DB session.")
        if ALLOW_DB_FAILURE and try_initialize_database(): # Attempt re-init
             logger.info("Visualisation DB - Re-initialization attempt made for get_db.")
        else:
            # If SessionLocal is None even after re-init attempt (or if not allowed), raise critical error.
            # This prevents the app from trying to operate without a DB session.
            raise Exception("Database not initialized for visualisation module. SessionLocal is None.")
            
    db = SessionLocal()
    try:
        log_connection_details("session_start", "attempted", {"session_id": id(db)})
        yield db
        log_connection_details("session_end", "success", {"session_id": id(db)})
    except Exception as e:
        log_connection_details("session_error", "failed", {"session_id": id(db), "error": str(e)})
        db.rollback() # Rollback on error
        raise
    finally:
        db.close()
        log_connection_details("session_close", "completed", {"session_id": id(db)})


def execute_query(query_str, params=None, timeout=30, max_retries=2):
    """
    Execute a raw SQL query and return the results as a list of dictionaries.
    This function remains useful for queries not easily expressed via ORM or for specific needs.
    """
    if not engine:
        logger.error("Visualisation DB - Engine not initialized. Cannot execute query.")
        if ALLOW_DB_FAILURE and try_initialize_database():
            logger.info("Visualisation DB - Re-initialization attempt made for execute_query.")
        else:
            raise Exception("Database engine not initialized for visualisation module.")
    operation = "execute_query"
    start_time = time.time()
    
    truncated_query = query_str[:500] + "..." if len(query_str) > 500 else query_str
    log_connection_details(operation, "attempted", {"query": truncated_query, "timeout": timeout})
    
    last_error = None
    for retry in range(max_retries + 1):
        if retry > 0:
            logger.info(f"Retry {retry}/{max_retries} for database query after {retry * 2} seconds delay")
            time.sleep(retry * 2)
        
        try:
            with time_limit(timeout): # Custom timeout context manager
                with engine.connect() as connection:
                    # For PostgreSQL, statement_timeout can be set per transaction or session.
                    # Setting it here ensures it applies to this specific query execution.
                    connection.execute(text(f"SET statement_timeout = {timeout * 1000}")) # ms
                    
                    result_proxy = connection.execute(text(query_str), params or {})
                    
                    # Check if the result_proxy has processable rows (e.g., for SELECT)
                    if result_proxy.returns_rows:
                        columns = result_proxy.keys()
                        rows = result_proxy.fetchall()
                        data = [dict(zip(columns, row)) for row in rows]
                        row_count = len(rows)
                    else: # For INSERT, UPDATE, DELETE that don't return rows by default
                        data = [] 
                        row_count = result_proxy.rowcount # Number of affected rows
                    
                    duration = time.time() - start_time
                    connection.commit() # Commit transaction if successful

                    log_connection_details(operation, "success", {
                        "rows_returned_or_affected": row_count,
                        "duration_ms": round(duration * 1000, 2),
                        "query_truncated": truncated_query,
                        "retries": retry
                    })
                    return data # Return list of dicts for SELECT, or empty list for others
        except TimeoutError as e: # Custom TimeoutError from time_limit context manager
            last_error = e
            duration = time.time() - start_time
            error_details = {"error_type": "TimeoutError", "error_msg": f"Query execution timed out after {timeout} seconds", "duration_ms": round(duration * 1000, 2), "query_truncated": truncated_query, "retry": retry}
            log_connection_details(operation, "timeout", error_details)
            logger.error(f"Query timed out after {timeout} seconds (retry {retry}/{max_retries}): {truncated_query}")
            if retry == max_retries:
                raise TimeoutError(f"Database query timed out after {timeout} seconds and {max_retries} retries")
        except Exception as e: # Catch other SQLAlchemy or DB errors
            last_error = e
            duration = time.time() - start_time
            error_details = {"error_type": type(e).__name__, "error_msg": str(e), "duration_ms": round(duration * 1000, 2), "query_truncated": truncated_query, "retry": retry, "traceback": traceback.format_exc()}
            log_connection_details(operation, "failed", error_details)
            logger.error(f"Error executing query (retry {retry}/{max_retries}): {e}", exc_info=True)
            if retry == max_retries:
                raise
    
    raise last_error or Exception("Unknown database error after retries in execute_query")


# New ORM-based data fetching functions
def get_train_cleaned_data_orm(db_session, filters=None, limit=None, columns_to_load=None):
    """
    Use ORM to query the train_cleaned table.
    Args:
        db_session: The SQLAlchemy session.
        filters: Dictionary of {attribute_name: value} for filtering.
        limit: Integer limit for the number of results.
        columns_to_load: Optional list of model attribute names to load (for efficiency).
    """
    logger.info(f"Visualisation DB - get_train_cleaned_data_orm received db_session of type: {type(db_session)}")
    if not db_session:
        logger.error("Visualisation DB - DB session not provided to get_train_cleaned_data_orm.")
        return []
    if not TrainCleaned:
        logger.error("Visualisation DB - TrainCleaned ORM model is not defined.")
        return []

    logger.info(f"Visualisation DB - Querying TrainCleaned with ORM. Filters: {filters}, Limit: {limit}, Columns to load: {columns_to_load}")
    try:
        query_select_entities = []
        actual_column_names_for_zip = []

        if columns_to_load:
            for col_name_str in columns_to_load:
                if hasattr(TrainCleaned, col_name_str):
                    query_select_entities.append(getattr(TrainCleaned, col_name_str))
                    actual_column_names_for_zip.append(col_name_str) # Use the attribute name for the dict key
                else:
                    logger.warning(f"Visualisation DB - Attribute {col_name_str} not found in TrainCleaned model, skipping for load_only.")
            if not query_select_entities: # If all requested columns were invalid
                logger.warning("Visualisation DB - No valid columns in columns_to_load for TrainCleaned, loading all attributes.")
                query = db_session.query(TrainCleaned) # Fallback to full object query
            else:
                query = db_session.query(*query_select_entities)
        else:
            query = db_session.query(TrainCleaned) # Default: query full object

        if filters:
            for attribute_name, value in filters.items():
                if hasattr(TrainCleaned, attribute_name):
                    column_attr = getattr(TrainCleaned, attribute_name)
                    if isinstance(value, list):
                        query = query.filter(column_attr.in_(value))
                    else:
                        query = query.filter(column_attr == value)
                else:
                    logger.warning(f"Visualisation DB - Filter attribute {attribute_name} not found in TrainCleaned model.")
        
        if limit:
            query = query.limit(limit)

        # Log the string representation of the query for TrainCleaned
        try:
            from sqlalchemy.dialects import postgresql
            compiled_query_str = str(query.statement.compile(dialect=postgresql.dialect(), compile_kwargs={"literal_binds": True}))
            logger.info(f"Visualisation DB - Compiled SQL for TrainCleaned: {compiled_query_str}")
        except Exception as e_compile:
            logger.error(f"Visualisation DB - Error compiling TrainCleaned query: {e_compile}", exc_info=True)
            logger.info(f"Visualisation DB - Basic query structure for TrainCleaned: {query}")
            
        results = query.all()
        
        data = []
        if query_select_entities: # If specific columns were queried (and at least one was valid)
            # `results` will be a list of Row objects (tuple-like)
            for row_tuple in results:
                data.append(dict(zip(actual_column_names_for_zip, row_tuple)))
        else: # Full model objects were queried (or columns_to_load was empty/all invalid)
            # Use column.key for both the dictionary key and getattr to use ORM attribute names
            processed_data = []
            column_attribute_keys = [] # Initialize
            if results: # Ensure there are results to inspect
                # Get mapper from the first object's class. Assuming all objects are of the same type.
                mapper = sqlalchemy_inspect(results[0].__class__)
                # Get a list of Python attribute names that correspond to columns
                column_attribute_keys = [prop.key for prop in mapper.iterate_properties 
                                         if isinstance(prop, ColumnProperty)]
            
            for row_obj in results:
                row_as_dict = {}
                for attr_key in column_attribute_keys: # Iterate using Python attribute names
                    try:
                        # For logging, find the DB column name this attribute maps to
                        db_column_name = "unknown_db_column"
                        if hasattr(mapper.attrs[attr_key], 'expression') and hasattr(mapper.attrs[attr_key].expression, 'name'):
                            db_column_name = mapper.attrs[attr_key].expression.name
                        
                        logger.info(f"{row_obj.__class__.__name__} - Accessing ORM attribute: '{attr_key}' (DB column: '{db_column_name}')")
                        value = getattr(row_obj, attr_key)
                        row_as_dict[attr_key] = value
                    except AttributeError as e_attr:
                        logger.error(f"{row_obj.__class__.__name__} - AttributeError for ORM attribute '{attr_key}': {e_attr}", exc_info=True)
                        # Optionally, put a placeholder or skip if an attribute is problematic
                        row_as_dict[attr_key] = f"ERROR_ACCESSING_{attr_key}" 
                processed_data.append(row_as_dict)
            data = processed_data

        logger.info(f"Visualisation DB - TrainCleaned ORM query returned {len(data)} rows.")
        return data
    except Exception as e:
        logger.error(f"Visualisation DB - Error querying TrainCleaned with ORM: {e}", exc_info=True)
        if ALLOW_DB_FAILURE:
            return []
        raise

def get_smmh_cleaned_data_orm(db_session, filters=None, limit=None, columns_to_load=None):
    """
    Use ORM to query the smmh_cleaned table.
    Args:
        db_session: The SQLAlchemy session.
        filters: Dictionary of {attribute_name: value} for filtering.
        limit: Integer limit for the number of results.
        columns_to_load: Optional list of model attribute names to load.
    """
    logger.info(f"Visualisation DB - get_smmh_cleaned_data_orm received db_session of type: {type(db_session)}")
    if not db_session:
        logger.error("Visualisation DB - DB session not provided to get_smmh_cleaned_data_orm.")
        # Raise an error immediately if no session, as ALLOW_DB_FAILURE is false by default
        raise ValueError("DB session not provided to get_smmh_cleaned_data_orm")
        
    if not SmmhCleaned:
        logger.error("Visualisation DB - SmmhCleaned ORM model is not defined.")
        raise ValueError("SmmhCleaned ORM model is not defined")

    logger.info(f"Visualisation DB - Querying SmmhCleaned with ORM. Filters: {filters}, Limit: {limit}, Columns to load: {columns_to_load}")
    try:
        query_select_entities = []
        actual_column_names_for_zip = []

        if columns_to_load:
            for col_name_str in columns_to_load:
                if hasattr(SmmhCleaned, col_name_str):
                    query_select_entities.append(getattr(SmmhCleaned, col_name_str))
                    actual_column_names_for_zip.append(col_name_str) # Use the attribute name
                else:
                    logger.warning(f"Visualisation DB - Attribute {col_name_str} not found in SmmhCleaned model, skipping for load_only.")
            if not query_select_entities: # If all requested columns were invalid
                logger.warning("Visualisation DB - No valid columns in columns_to_load for SmmhCleaned, loading all attributes.")
                query = db_session.query(SmmhCleaned) # Fallback
            else:
                query = db_session.query(*query_select_entities)
        else:
            query = db_session.query(SmmhCleaned) # Default: query full object

        if filters:
            for attribute_name, value in filters.items():
                if hasattr(SmmhCleaned, attribute_name):
                    column_attr = getattr(SmmhCleaned, attribute_name)
                    if isinstance(value, list):
                        query = query.filter(column_attr.in_(value))
                    else:
                        query = query.filter(column_attr == value)
                else:
                    logger.warning(f"Visualisation DB - Filter attribute {attribute_name} not found in SmmhCleaned model.")

        if limit:
            query = query.limit(limit)
        
        # Log the string representation of the query
        try:
            # Ensure the dialect is appropriate (e.g., postgresql for PostgreSQL)
            from sqlalchemy.dialects import postgresql
            compiled_query_str = str(query.statement.compile(dialect=postgresql.dialect(), compile_kwargs={"literal_binds": True}))
            logger.info(f"Visualisation DB - Compiled SQL for SmmhCleaned: {compiled_query_str}")
        except Exception as e_compile:
            logger.error(f"Visualisation DB - Error compiling SmmhCleaned query: {e_compile}", exc_info=True)
            # Log a simpler version if advanced compilation fails
            logger.info(f"Visualisation DB - Basic query structure for SmmhCleaned: {query}")
        results = query.all()

        data = []
        if query_select_entities: # If specific columns were queried
            for row_tuple in results:
                data.append(dict(zip(actual_column_names_for_zip, row_tuple)))
        else: # Full model objects were queried
            # Use column.key for both the dictionary key and getattr to use ORM attribute names
            processed_data = []
            column_attribute_keys = [] # Initialize
            if results: # Ensure there are results to inspect
                # Get mapper from the first object's class. Assuming all objects are of the same type.
                mapper = sqlalchemy_inspect(results[0].__class__)
                # Get a list of Python attribute names that correspond to columns
                column_attribute_keys = [prop.key for prop in mapper.iterate_properties
                                         if isinstance(prop, ColumnProperty)]
            
            for row_obj in results:
                row_as_dict = {}
                for attr_key in column_attribute_keys: # Iterate using Python attribute names
                    try:
                        # For logging, find the DB column name this attribute maps to
                        db_column_name = "unknown_db_column"
                        if hasattr(mapper.attrs[attr_key], 'expression') and hasattr(mapper.attrs[attr_key].expression, 'name'):
                            db_column_name = mapper.attrs[attr_key].expression.name

                        logger.info(f"{row_obj.__class__.__name__} - Accessing ORM attribute: '{attr_key}' (DB column: '{db_column_name}')")
                        value = getattr(row_obj, attr_key)
                        row_as_dict[attr_key] = value
                    except AttributeError as e_attr:
                        logger.error(f"{row_obj.__class__.__name__} - AttributeError for ORM attribute '{attr_key}': {e_attr}", exc_info=True)
                        # Optionally, put a placeholder or skip if an attribute is problematic
                        row_as_dict[attr_key] = f"ERROR_ACCESSING_{attr_key}"
                processed_data.append(row_as_dict)
            data = processed_data
            
        logger.info(f"Visualisation DB - SmmhCleaned ORM query returned {len(data)} rows.")
        return data
    except Exception as e:
        logger.error(f"Visualisation DB - Error querying SmmhCleaned with ORM (THIS IS THE LIKELY CULPRIT): {e}", exc_info=True)
        # Since ALLOW_DB_FAILURE defaults to False, we should re-raise to ensure it's not caught by a misconfigured ALLOW_DB_FAILURE=True scenario.
        # If ALLOW_DB_FAILURE was True, the original code would return [].
        # Forcing a raise here ensures the error is propagated if it's the cause of transaction abortion.
        raise # Re-raise the caught exception 