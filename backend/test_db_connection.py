#!/usr/bin/env python3
"""
Database connection test script

This script attempts to connect to the PostgreSQL database and runs some
basic queries to verify connectivity and data access.
"""

import os
import sys
import time
import logging
import argparse
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError
from dotenv import load_dotenv

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("db_test")

def mask_db_url(url):
    """Mask password in database URL for logging"""
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

def test_connection(db_url, timeout=30, verbose=False):
    """Test database connection and run basic queries"""
    start_time = time.time()
    
    logger.info(f"Testing connection to {mask_db_url(db_url)}")
    logger.info(f"Connection timeout: {timeout} seconds")
    
    # Create engine with improved settings for Railway PostgreSQL
    try:
        engine = create_engine(
            db_url,
            pool_size=5,
            max_overflow=10,
            pool_timeout=timeout,
            pool_recycle=300,
            pool_pre_ping=True,
            connect_args={
                "connect_timeout": timeout,
                "keepalives": 1,
                "keepalives_idle": 30,
                "keepalives_interval": 10,
                "keepalives_count": 5,
                "options": f"-c statement_timeout={timeout * 1000}"
            }
        )
        
        # Test basic connection
        logger.info("Testing basic connection...")
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
            logger.info("✅ Basic connection successful")
        
        # List all tables
        logger.info("Listing tables...")
        with engine.connect() as conn:
            result = conn.execute(text(
                "SELECT table_name FROM information_schema.tables "
                "WHERE table_schema = 'public'"
            ))
            tables = [row[0] for row in result]
            
            if verbose:
                logger.info(f"Found {len(tables)} tables: {', '.join(tables)}")
            else:
                logger.info(f"Found {len(tables)} tables")
        
        # Test specific tables needed for visualisation
        required_tables = ['train_cleaned', 'smmh_cleaned']
        for table in required_tables:
            if table in tables:
                logger.info(f"Testing {table} table...")
                with engine.connect() as conn:
                    # Check row count
                    result = conn.execute(text(f"SELECT COUNT(*) FROM {table}"))
                    count = result.scalar()
                    logger.info(f"✅ {table} table exists with {count} rows")
                    
                    # Preview data (first 5 rows)
                    if verbose and count > 0:
                        result = conn.execute(text(f"SELECT * FROM {table} LIMIT 5"))
                        columns = result.keys()
                        rows = [dict(zip(columns, row)) for row in result]
                        logger.info(f"First 5 rows from {table}:")
                        for row in rows:
                            logger.info(f"  {row}")
            else:
                logger.error(f"❌ Required table '{table}' not found")
        
        duration = time.time() - start_time
        logger.info(f"All tests completed in {duration:.2f} seconds")
        return True
        
    except SQLAlchemyError as e:
        duration = time.time() - start_time
        logger.error(f"❌ Database connection failed after {duration:.2f} seconds")
        logger.error(f"Error: {e}")
        return False

def main():
    parser = argparse.ArgumentParser(description="Test PostgreSQL database connection")
    parser.add_argument("--db-url", help="Database URL (overrides environment variable)")
    parser.add_argument("--timeout", type=int, default=30, help="Connection timeout in seconds")
    parser.add_argument("--verbose", action="store_true", help="Show detailed output")
    args = parser.parse_args()
    
    # Load environment variables
    load_dotenv()
    
    # Get DATABASE_URL from args or environment
    db_url = args.db_url or os.getenv("DATABASE_URL", "postgresql://postgres:postgres@postgres-production-7575.up.railway.app:5432/railway")
    
    # Handle Railway PostgreSQL URLs
    if "postgres://" in db_url:
        db_url = db_url.replace("postgres://", "postgresql://")
    
    success = test_connection(db_url, args.timeout, args.verbose)
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main() 