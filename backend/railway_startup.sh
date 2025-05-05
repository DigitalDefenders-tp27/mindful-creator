#!/usr/bin/env bash
set -e

echo "[startup] Mindful-Creator – waiting 5s for cold-boot..."
sleep 5

APP_PORT="${PORT:-8000}"      # Railway 注入 PORT=8000
echo "[startup] Launching Uvicorn on ${APP_PORT}"

exec uvicorn app.main:app \
     --host 0.0.0.0 \
     --port "${APP_PORT}" \
     --workers 1 \
     --log-level info