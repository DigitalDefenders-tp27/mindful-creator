from fastapi import APIRouter
from backend.app.api.games.memory_match import router as memory_match_router

router = APIRouter()

router.include_router(memory_match_router, prefix="/memory-match", tags=["games"]) 