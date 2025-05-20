#!/usr/bin/env python3
"""
Railway PostgreSQL database connection test

This script tests the connection to the Railway PostgreSQL database
using the DATABASE_PUBLIC_URL environment variable.
"""

import os
import sys
import time
import logging
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("railway_db_test")

def main():
    # Load environment variables
    load_dotenv()
    
    # Prioritize DATABASE_PUBLIC_URL, then DATABASE_URL
    db_url = os.getenv("DATABASE_PUBLIC_URL") or os.getenv("DATABASE_URL")
    
    if not db_url:
        logger.error("Neither DATABASE_PUBLIC_URL nor DATABASE_URL environment variables are set.")
        sys.exit(1)
    
    # Log which variable is being used
    if os.getenv("DATABASE_PUBLIC_URL"):
        logger.info("Using DATABASE_PUBLIC_URL.")
    elif os.getenv("DATABASE_URL"):
        logger.info("Using DATABASE_URL as fallback.")

    # Handle Railway PostgreSQL URLs
    if "postgres://" in db_url:
        db_url = db_url.replace("postgres://", "postgresql://")
        logger.info("Converted postgres:// URL to postgresql://")
    
    # Mask password for logging
    masked_url = db_url
    if "@" in db_url:
        parts = db_url.split("@")
        auth_parts = parts[0].split("//")
        if len(auth_parts) >= 2:
            protocol = auth_parts[0]
            auth = auth_parts[1].split(":")
            user = auth[0] if auth else "unknown"
            masked_url = f"{protocol}//{user}:****@{parts[1]}"
    
    logger.info(f"Testing connection to: {masked_url}")
    
    try:
        # Create engine with increased timeouts
        logger.info("Creating SQLAlchemy engine...")
        engine = create_engine(
            db_url,
            pool_pre_ping=True,
            connect_args={
                "connect_timeout": 30,
                "keepalives": 1,
                "keepalives_idle": 30,
                "keepalives_interval": 10,
                "keepalives_count": 5,
                "options": "-c statement_timeout=30000"
            }
        )
        
        # Test basic connection
        logger.info("Testing basic connection...")
        start_time = time.time()
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
            duration = time.time() - start_time
            logger.info(f"✅ Connection successful! ({duration:.2f}s)")
        
        # List all tables
        logger.info("Listing tables...")
        start_time = time.time()
        with engine.connect() as conn:
            result = conn.execute(text(
                "SELECT table_name FROM information_schema.tables "
                "WHERE table_schema = 'public'"
            ))
            tables = [row[0] for row in result]
            duration = time.time() - start_time
            logger.info(f"Found {len(tables)} tables: {', '.join(tables)} ({duration:.2f}s)")
        
        # Test specific tables required for visualization
        required_tables = ['train_cleaned', 'smmh_cleaned']
        for table in required_tables:
            if table in tables:
                logger.info(f"Testing {table} table...")
                start_time = time.time()
                with engine.connect() as conn:
                    result = conn.execute(text(f"SELECT COUNT(*) FROM {table}"))
                    count = result.scalar()
                    duration = time.time() - start_time
                    logger.info(f"✅ {table} table exists with {count} rows ({duration:.2f}s)")
            else:
                logger.error(f"❌ Required table '{table}' not found in database")
        
        logger.info("All connection tests passed successfully!")
        return 0
        
    except Exception as e:
        logger.error(f"❌ Database connection failed: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    sys.exit(main()) 