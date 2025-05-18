# backend/app/api/data/routes.py

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import TrainCleaned

router = APIRouter(
    prefix="/analytics",
    tags=["Analytics"]
)
