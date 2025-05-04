#!/usr/bin/env bash
set -euo pipefail

# ---------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------
APP_PORT="${PORT:-8000}"      # Railway 会传 PORT，没传就用 8000
BOOT_DELAY="${BOOT_DELAY:-5}" # 如需更长/更短延迟，部署变量里调 BOOT_DELAY

# ---------------------------------------------------------------
# Startup sequence
# ---------------------------------------------------------------
echo "[$(date '+%F %T')] Mindful-Creator startup script"
echo "→ Waiting ${BOOT_DELAY}s so routes are ready before health-check…"
sleep "${BOOT_DELAY}"

echo "→ Launching Uvicorn on port ${APP_PORT}"
exec uvicorn app.main:app              \
     --host 0.0.0.0                    \
     --port "${APP_PORT}"              \
     --workers 1                       \
     --log-level info