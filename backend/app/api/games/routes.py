from fastapi import APIRouter
from backend.app.api.games.memory_match import router as memory_match_router

router = APIRouter()

router.include_router(memory_match_router, prefix="/memory-match", tags=["games"])

# Add direct route for scanning memes (separate from memory-match prefix)
from backend.app.api.games.memory_match import scan_available_memes
router.add_api_route("/memes/available", scan_available_memes, methods=["GET"], tags=["memes"], description="Get list of available meme images") 