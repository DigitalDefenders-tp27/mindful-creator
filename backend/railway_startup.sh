#!/usr/bin/env bash
set -e

echo ">> current dir $(pwd)"
echo ">> PORT from Railway = ${PORT:-unset}"

APP_PORT=8080                       # ***绝不能再改成 8000***
echo ">> starting Uvicorn on ${APP_PORT}"

exec uvicorn app.main:app \
     --host 0.0.0.0 \
     --port "${APP_PORT}" \
     --workers 1 \
     --log-level info