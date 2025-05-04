#!/usr/bin/env bash
set -euo pipefail

###############################################################################
# Mindful-Creator Railway start script
###############################################################################

# ── 配置 —— ---------------------------------------------------------------
APP_PORT="${PORT:-8000}"          # Railway 会自动注入 PORT；本地跑就用 8000
BOOT_DELAY="${BOOT_DELAY:-5}"     # 给 FastAPI 路由 5s 时间挂载，避免探活 404
LOG_TS() { date '+%F %T'; }

# ── 启动流程 —— -----------------------------------------------------------
echo "[$(LOG_TS)] Mindful-Creator startup script"
echo "→ Waiting ${BOOT_DELAY}s so routes are ready before health-check…"
sleep "${BOOT_DELAY}"

echo "→ Launching Uvicorn on port ${APP_PORT}"
exec uvicorn app.main:app \
     --host 0.0.0.0        \
     --port "${APP_PORT}"  \
     --workers 1           \
     --log-level info