#!/usr/bin/env bash
set -e

echo "[startup] Mindful-Creator – Railway Deployment"

# Check and install missing dependencies
echo "[startup] Checking for missing dependencies..."
pip install httpx>=0.24.0 psycopg2-binary>=2.9.6 tenacity>=8.2.0 --no-cache-dir

# Set environment variables to ensure the app starts even if DB is not accessible
export ALLOW_DB_FAILURE=true
export DATABASE_CONNECT_TIMEOUT=30
export APP_STARTUP_TIMEOUT=30
export MAX_DB_RETRIES=5

# Set port from Railway environment or default
APP_PORT="${PORT:-8000}"
echo "[startup] Will launch Uvicorn on port ${APP_PORT}"

# Function to test database connectivity in background
test_db_connection() {
  echo "[startup] Testing database connectivity using $1 (background)..."
  python -c "
import sys, os, time, traceback
from sqlalchemy import create_engine, text
from tenacity import retry, wait_exponential, stop_after_attempt

@retry(wait=wait_exponential(multiplier=1, min=2, max=10), stop=stop_after_attempt(${MAX_DB_RETRIES}))
def test_db_connection():
    print('[DB Test] Attempting to connect to database...')
    db_url = os.environ.get('$1', '')
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
    return True

try:
    result = test_db_connection()
    print(f'[DB Test] Final result: {result}')
except Exception as e:
    print('[DB Test] Database connection failed after retries:', e)
    traceback.print_exc()
    print('[DB Test] App will continue to start regardless of database status (ALLOW_DB_FAILURE=true)')
" &
}

# Check if the database URL is provided
if [ -n "${DATABASE_PUBLIC_URL}" ]; then
  echo "[startup] DATABASE_PUBLIC_URL is configured"
  # Export as DATABASE_URL for backward compatibility
  export DATABASE_URL="${DATABASE_PUBLIC_URL}"
  
  # Test database connectivity but don't block startup
  test_db_connection "DATABASE_PUBLIC_URL"
elif [ -n "${DATABASE_URL}" ]; then
  echo "[startup] DATABASE_URL is configured"
  
  # Test database connectivity but don't block startup
  test_db_connection "DATABASE_URL"
else
  echo "[startup] WARNING: No database URL environment variables (DATABASE_PUBLIC_URL or DATABASE_URL) provided"
fi

# Create a lightweight health check endpoint
echo "[startup] Creating lightweight pre-startup health endpoint"
mkdir -p /tmp/health_app
cat > /tmp/health_app/app.py << EOF
from fastapi import FastAPI
from fastapi.responses import JSONResponse
import uvicorn
import os

app = FastAPI()

@app.get("/health")
def health():
    return JSONResponse(content={"status": "ok"})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("app:app", host="0.0.0.0", port=port)
EOF

# Start the lightweight health app in the background and save its PID
python -m uvicorn /tmp/health_app.app:app --host 0.0.0.0 --port "${APP_PORT}" &
HEALTH_APP_PID=$!
echo "[startup] Lightweight health app started with PID: ${HEALTH_APP_PID}"

# Give the lightweight app a moment to start
sleep 2

echo "[startup] Launching Uvicorn with increased timeouts"
# Kill the lightweight health app before starting the main app
kill $HEALTH_APP_PID || true

exec uvicorn app.main:app \
     --host 0.0.0.0 \
     --port "${APP_PORT}" \
     --workers 1 \
     --log-level info \
     --timeout-keep-alive 120