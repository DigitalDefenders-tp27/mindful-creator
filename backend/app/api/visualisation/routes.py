from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from typing import Dict, Any

from . import data_processors

router = APIRouter(
    prefix="/api/visualisation",
    tags=["visualisation"],
    responses={404: {"description": "Not found"}},
)

@router.get("/screen-time-emotions")
async def get_screen_time_emotions() -> Dict[str, Any]:
    """
    Get data for screen time vs emotions chart
    """
    try:
        data = data_processors.process_screen_time_emotions()
        return JSONResponse(content=data)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve screen time emotions data: {str(e)}"
        )

@router.get("/sleep-quality")
async def get_sleep_quality() -> Dict[str, Any]:
    """
    Get data for digital habits vs sleep quality chart
    """
    try:
        data = data_processors.process_sleep_data()
        return JSONResponse(content=data)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve sleep quality data: {str(e)}"
        )

@router.get("/engagement")
async def get_engagement() -> Dict[str, Any]:
    """
    Get data for engagement metrics chart
    """
    try:
        data = data_processors.process_engagement_data()
        return JSONResponse(content=data)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve engagement data: {str(e)}"
        )

@router.get("/anxiety")
async def get_anxiety() -> Dict[str, Any]:
    """
    Get data for screen time vs anxiety chart
    """
    try:
        data = data_processors.process_anxiety_data()
        return JSONResponse(content=data)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve anxiety data: {str(e)}"
        )

@router.get("/all-chart-data")
async def get_all_chart_data() -> Dict[str, Any]:
    """
    Get data for all charts in a single request
    """
    try:
        return {
            "screenTimeEmotions": data_processors.process_screen_time_emotions(),
            "sleepQuality": data_processors.process_sleep_data(),
            "engagement": data_processors.process_engagement_data(),
            "anxiety": data_processors.process_anxiety_data()
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve all chart data: {str(e)}"
        ) 