from fastapi import APIRouter
from .memory_match import router as memory_match_router

router = APIRouter()

router.include_router(memory_match_router, prefix="/memory_match", tags=["Memory Match"])

# Add direct route for scanning memes (separate from memory-match prefix)
from .memory_match import scan_available_memes
router.add_api_route("/memes/available", scan_available_memes, methods=["GET"], tags=["memes"], description="Get list of available meme images") 