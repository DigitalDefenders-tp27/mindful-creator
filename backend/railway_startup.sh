#!/usr/bin/env bash
set -e

echo ">> current dir $(pwd)"
echo ">> PORT from Railway = ${PORT:-unset}"

 # never change this
APP_PORT="${PORT:-8000}"        
echo "Starting Uvicorn on $APP_PORT …"

exec uvicorn app.main:app \
     --host 0.0.0.0 \
     --port "$APP_PORT" \
     --workers 1 \
     --log-level info