from fastapi import APIRouter
from backend.app.api.endpoints import youtube, websocket, relaxation
from backend.app.api.games.routes import router as games_router

api_router = APIRouter()
api_router.include_router(youtube.router, prefix="/youtube", tags=["youtube"])
api_router.include_router(websocket.router, prefix="/websocket", tags=["websocket"])
api_router.include_router(relaxation.router, prefix="/relaxation", tags=["relaxation"])
api_router.include_router(games_router, prefix="/games", tags=["games"]) 