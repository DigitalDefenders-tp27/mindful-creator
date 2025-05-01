import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.youtube.routes import router as youtube_router
from app.api.data.routes import router as data_router
from .routes import relaxation

# Create FastAPI application
app = FastAPI(
    title="Mindful Creator API",
    description="YouTube Comment Analysis API",
    version="1.0.0"
)

# Configure CORS
origins = [
    os.getenv("CORS_ORIGIN", "http://localhost:3000"),
    "http://localhost:5173",
    "http://localhost:5174",
    "http://localhost:5175",
    "https://mindful-creator-awoc.vercel.app",
    "https://mindful-creator-mymc.vercel.app",
    "https://mindful-creator-gwnq.vercel.app",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routes
app.include_router(youtube_router, prefix="/api/youtube", tags=["youtube"])
app.include_router(data_router, prefix="/api", tags=["data"])
app.include_router(relaxation.router, prefix="/api", tags=["relaxation"])

@app.get("/")
async def root():
    return {"message": "Mindful Creator API is running"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True) 
