# app/api/router.py
import os, sys, time, platform, logging, psutil
from datetime import datetime
from typing import Dict, Any

from fastapi import APIRouter, Request, HTTPException

router = APIRouter()
logger = logging.getLogger(__name__)

# ------------------------------------------------------------------
# 根路由 —— 简单存活探针
# ------------------------------------------------------------------
@router.get("/")
async def api_root() -> Dict[str, str]:
    logger.info("API root endpoint accessed")
    return {"status": "alive"}

# ------------------------------------------------------------------
# 健康检查实现（供 GET / POST 共用）
# ------------------------------------------------------------------
async def _health_payload(request: Request) -> Dict[str, Any]:
    t0 = time.time()

    # ── 进程 / 系统资源 ───────────────────────────────────────────
    proc   = psutil.Process(os.getpid())
    vmem   = psutil.virtual_memory()
    rss_mb = round(proc.memory_info().rss / 1024 / 1024, 2)
    vms_mb = round(proc.memory_info().vms / 1024 / 1024, 2)
    cpu_pct = round(proc.cpu_percent(interval=0.1), 2)

    # ── App.state 中的模型信息 ────────────────────────────────────
    model_loaded = getattr(request.app.state, "model_loaded", False)

    # ── 其他环境变量 ──────────────────────────────────────────────
    youtube_key_ok = bool(os.getenv("YOUTUBE_API_KEY"))

    return {
        "status": "ok",
        "timestamp": datetime.utcnow().isoformat(),
        "environment": {
            "python_version": platform.python_version(),
            "platform": platform.platform(),
            "process_id": os.getpid()
        },
        "resources": {
            "memory_rss_mb": rss_mb,
            "memory_vms_mb": vms_mb,
            "cpu_percent": cpu_pct,
            "system_memory_total_gb": round(vmem.total / 1024 / 1024 / 1024, 2),
            "system_memory_available_gb": round(vmem.available / 1024 / 1024 / 1024, 2),
            "system_memory_percent": round(vmem.percent, 2),
        },
        "features": {
            "model_loaded": model_loaded,
            "youtube_api_available": youtube_key_ok,
        },
        "uptime_seconds": round(time.time() - proc.create_time(), 2),
        "response_time_ms": round((time.time() - t0) * 1000, 2),
    }

# ------------------------------------------------------------------
# GET /health  —— 供 Railway / 浏览器探活
# ------------------------------------------------------------------
@router.get("/health")
async def health_get(request: Request):
    logger.info("GET /health accessed")
    return await _health_payload(request)

# ------------------------------------------------------------------
# POST /health —— 供前端 fetch POST 健康检查
# ------------------------------------------------------------------
@router.post("/health")
async def health_post(request: Request):
    logger.info("POST /health accessed")
    return await _health_payload(request)