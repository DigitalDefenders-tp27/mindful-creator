# app/api/router.py
import os, time, platform, logging, psutil
from datetime import datetime
from typing import Dict, Any

from fastapi import APIRouter, Request
from pydantic import BaseModel

_LOG = logging.getLogger("api.router")

router = APIRouter()

# ──────────────────────────────────────────────────────────────
# Pydantic schema 便于 openapi & front-end 类型推断
# ──────────────────────────────────────────────────────────────
class HealthPayload(BaseModel):
    status: str
    timestamp: str
    environment: Dict[str, Any]
    resources: Dict[str, Any]
    features: Dict[str, Any]
    uptime_seconds: float
    response_time_ms: float

# ──────────────────────────────────────────────────────────────
# /           —— very light liveness probe
# ──────────────────────────────────────────────────────────────
@router.get("/", tags=["misc"], summary="Root probe")
async def api_root() -> Dict[str, str]:
    _LOG.info("GET / (root) hit")
    return {"status": "alive"}

# ──────────────────────────────────────────────────────────────
# /health   —— single source of truth for Railway & FE
# ──────────────────────────────────────────────────────────────
def _collect_health(app_state, start_t: float) -> Dict[str, Any]:
    proc   = psutil.Process(os.getpid())
    vmem   = psutil.virtual_memory()

    return {
        "status": "ok",
        "timestamp": datetime.utcnow().isoformat(),
        "environment": {
            "python_version": platform.python_version(),
            "platform":       platform.platform(),
            "pid":            os.getpid(),
        },
        "resources": {
            "memory_rss_mb": round(proc.memory_info().rss / 1024 / 1024, 2),
            "cpu_percent":   round(proc.cpu_percent(0.1), 2),
            "system_mem_pct": round(vmem.percent, 2),
        },
        "features": {
            "model_loaded": getattr(app_state, "model_loaded", False),
            "youtube_api_available": bool(os.getenv("YOUTUBE_API_KEY")),
        },
        "uptime_seconds": round(time.time() - proc.create_time(), 2),
        "response_time_ms": round((time.time() - start_t) * 1000, 2),
    }

@router.get(
    "/health",
    tags=["health"],
    response_model=HealthPayload,
    summary="Health check (GET)",
    status_code=200,
)
async def health_get(request: Request):
    _LOG.debug("GET /health hit")
    t0 = time.time()
    return _collect_health(request.app.state, t0)

# 如前端一定要 POST，取消下面注释即可
# @router.post(
#     "/health",
#     tags=["health"],
#     response_model=HealthPayload,
#     summary="Health check (POST)",
#     status_code=200,
# )
# async def health_post(request: Request):
#     _LOG.debug("POST /health hit")
#     t0 = time.time()
#     return _collect_health(request.app.state, t0)