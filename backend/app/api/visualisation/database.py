import os
import logging
import traceback
import sys
import json
import time
from sqlalchemy import create_engine, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("visualisation.database")

# Get DATABASE_URL from environment variables
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@postgres-production-7575.up.railway.app:5432/railway")

# Handle Railway PostgreSQL URLs
if "postgres://" in DATABASE_URL:
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://")

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

# Database connection engine and session factory
try:
    # Create database engine with PostgreSQL-specific settings
    engine = create_engine(
        DATABASE_URL,
        pool_size=5,
        max_overflow=10,
        pool_timeout=30,
        pool_recycle=1800,
        pool_pre_ping=True
    )
    
    # Create session factory
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    
    # Create base class
    Base = declarative_base()
    
    logger.info("Database engine created successfully")
except Exception as e:
    logger.error(f"Error creating database engine: {e}")
    logger.error(traceback.format_exc())
    raise

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

def execute_query(query_str, params=None):
    """Execute a raw SQL query and return the results as a list of dictionaries"""
    operation = "execute_query"
    start_time = time.time()
    
    # Log the query being attempted (truncate if too long)
    truncated_query = query_str[:500] + "..." if len(query_str) > 500 else query_str
    log_connection_details(operation, "attempted", {"query": truncated_query})
    
    try:
        with engine.connect() as connection:
            result = connection.execute(text(query_str), params or {})
            columns = result.keys()
            rows = result.fetchall()
            duration = time.time() - start_time
            
            # Log successful query execution
            row_count = len(rows)
            log_connection_details(operation, "success", {
                "rows_returned": row_count,
                "duration_ms": round(duration * 1000, 2),
                "query_truncated": truncated_query
            })
            
            return [dict(zip(columns, row)) for row in rows]
    except Exception as e:
        # Log the failure with detailed error info
        duration = time.time() - start_time
        error_details = {
            "error_type": type(e).__name__,
            "error_msg": str(e),
            "duration_ms": round(duration * 1000, 2),
            "query_truncated": truncated_query,
            "traceback": traceback.format_exc()
        }
        log_connection_details(operation, "failed", error_details)
        logger.error(f"Error executing query: {e}")
        logger.error(f"Query was: {query_str}")
        raise 