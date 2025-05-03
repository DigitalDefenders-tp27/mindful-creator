#!/usr/bin/env bash
set -e
APP_PORT=8080
echo "Starting Uvicorn on port $APP_PORT ..."
exec uvicorn app.main:app --host 0.0.0.0 --port "$APP_PORT" --workers 1 --log-level info

APP_PORT="${PORT:-8000}"
echo "Starting Uvicorn on port $APP_PORT …"
exec uvicorn app.main:app --host 0.0.0.0 --port "$APP_PORT" --workers 1 --log-level info

MODEL_DIR="app/nlp"
if [[ -f "$MODEL_DIR/app.py" ]]; then
  echo "✅ NLP model found"
  export MODEL_LOADED=true
else
  echo "⚠️  NLP model NOT found, limited functionality"
  export MODEL_LOADED=false
fi

echo "Current dir: $(pwd)"
echo "Model dir listing:"
ls -la "$MODEL_DIR"

echo "Starting Uvicorn on $APP_PORT ..."
exec uvicorn app.main:app --host 0.0.0.0 --port "$APP_PORT" --workers 1 --log-level info
echo "PORT env from Railway = ${PORT}"