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

# Set port from Railway environment or default
APP_PORT="${PORT:-8000}"
echo "[startup] Will launch Uvicorn on port ${APP_PORT}"

# Check if the database URL is provided
if [ -n "${DATABASE_PUBLIC_URL}" ]; then
  echo "[startup] DATABASE_PUBLIC_URL is configured"
  # Export as DATABASE_URL for backward compatibility
  export DATABASE_URL="${DATABASE_PUBLIC_URL}"
elif [ -n "${DATABASE_URL}" ]; then
  echo "[startup] DATABASE_URL is configured"
else
  echo "[startup] WARNING: No database URL environment variables (DATABASE_PUBLIC_URL or DATABASE_URL) provided"
fi

# Ensure we're in the correct directory structure
# Get the absolute path to the script's directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
echo "[startup] Script directory: ${SCRIPT_DIR}"

# Move to the script directory
cd "$SCRIPT_DIR"
echo "[startup] Changed working directory to: $(pwd)"

# Create a proper Python module structure
# Railway deployment may place files in unexpected locations, so we need to ensure 
# the app module is in the Python path
export PYTHONPATH="$SCRIPT_DIR:$PYTHONPATH"
echo "[startup] Set PYTHONPATH: $PYTHONPATH"

# Dump environment variables for debugging
echo "[startup] Environment variables:"
env | grep -E "DATABASE|PYTHON|PATH|PORT|ALLOW" || true

# Launch the application with proper module access
echo "[startup] Starting application with direct module access"
export PYTHONUNBUFFERED=1  # Make sure Python output is not buffered
exec python -m uvicorn app.main:app --host 0.0.0.0 --port "${APP_PORT}" --log-level debug