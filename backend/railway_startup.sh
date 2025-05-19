#!/usr/bin/env bash
set -e

echo "[startup] Mindful-Creator – Railway Deployment"

# Check and install missing dependencies
echo "[startup] Checking for missing dependencies..."
pip install httpx>=0.24.0 psycopg2-binary>=2.9.6 --no-cache-dir

# Set environment variables to ensure the app starts even if DB is not accessible
export ALLOW_DB_FAILURE=true
export DATABASE_CONNECT_TIMEOUT=30
export APP_STARTUP_TIMEOUT=20

# Set port from Railway environment or default
APP_PORT="${PORT:-8000}"
echo "[startup] Will launch Uvicorn on port ${APP_PORT}"

# Check if the database URL is provided
if [ -n "${DATABASE_PUBLIC_URL}" ]; then
  echo "[startup] DATABASE_PUBLIC_URL is configured"
  # Export as DATABASE_URL for backward compatibility
  export DATABASE_URL="${DATABASE_PUBLIC_URL}"
  
  # Test database connectivity but don't block startup
  echo "[startup] Testing database connectivity using DATABASE_PUBLIC_URL (background)..."
  python -c "
import sys, os, time, traceback
from sqlalchemy import create_engine, text
try:
    print('[DB Test] Attempting to connect to database...')
    db_url = os.environ.get('DATABASE_PUBLIC_URL', '')
    if 'postgres://' in db_url:
        db_url = db_url.replace('postgres://', 'postgresql://')
    engine = create_engine(
        db_url, 
        pool_pre_ping=True,
        connect_args={'connect_timeout': 15}
    )
    with engine.connect() as conn:
        result = conn.execute(text('SELECT 1'))
        print('[DB Test] Database connection successful!')
except Exception as e:
    print('[DB Test] Database connection failed:', e)
    traceback.print_exc()
    # Don't exit with error - app should still start
" &
elif [ -n "${DATABASE_URL}" ]; then
  echo "[startup] DATABASE_URL is configured"
  
  # Test database connectivity but don't block startup
  echo "[startup] Testing database connectivity using DATABASE_URL (background)..."
  python -c "
import sys, os, time, traceback
from sqlalchemy import create_engine, text
try:
    print('[DB Test] Attempting to connect to database...')
    db_url = os.environ.get('DATABASE_URL', '')
    if 'postgres://' in db_url:
        db_url = db_url.replace('postgres://', 'postgresql://')
    engine = create_engine(
        db_url, 
        pool_pre_ping=True,
        connect_args={'connect_timeout': 15}
    )
    with engine.connect() as conn:
        result = conn.execute(text('SELECT 1'))
        print('[DB Test] Database connection successful!')
except Exception as e:
    print('[DB Test] Database connection failed:', e)
    traceback.print_exc()
    # Don't exit with error - app should still start
" &
else
  echo "[startup] WARNING: No database URL environment variables (DATABASE_PUBLIC_URL or DATABASE_URL) provided"
fi

echo "[startup] Launching Uvicorn"
exec uvicorn app.main:app \
     --host 0.0.0.0 \
     --port "${APP_PORT}" \
     --workers 1 \
     --log-level info \
     --timeout-keep-alive 120