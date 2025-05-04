#!/usr/bin/env bash
set -e

echo "Current dir: $(pwd)"
echo "PORT env from Railway = ${PORT:-unset}"   # 仅打印

# 检测 NLP 模型文件
MODEL_DIR="app/nlp"
if [ -f "$MODEL_DIR/app.py" ]; then
  echo "✅ NLP model found"
else
  echo "⚠️  NLP model NOT found, limited functionality"
fi

echo "Dir listing:"
ls -la "$MODEL_DIR"

APP_PORT=8080             # 容器必须监听 8080
echo "Starting Uvicorn on port $APP_PORT ..."
exec uvicorn app.main:app --host 0.0.0.0 --port "$APP_PORT" --workers 1 --log-level info