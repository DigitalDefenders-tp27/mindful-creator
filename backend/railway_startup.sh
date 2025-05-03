#!/usr/bin/env bash
set -e

# 使用Railway提供的PORT环境变量，如果未设置则默认为8000
APP_PORT="${PORT:-8000}"
echo "PORT env from Railway = ${PORT:-not set}"
echo "Using port: $APP_PORT"
echo "Current dir: $(pwd)"

MODEL_DIR="app/nlp"
if [[ -f "$MODEL_DIR/app.py" ]]; then
  echo "✅ NLP model found"
  export MODEL_LOADED=true
else
  echo "⚠️  NLP model NOT found, limited functionality"
  export MODEL_LOADED=false
fi

echo "Model dir listing:"
ls -la "$MODEL_DIR"

echo "Starting Uvicorn on port $APP_PORT ..."
exec uvicorn app.main:app \
     --host 0.0.0.0 \
     --port "$APP_PORT" \
     --workers 1 \
     --log-level info