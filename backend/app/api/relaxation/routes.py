from fastapi import APIRouter
from typing import Dict, List, Any

router = APIRouter()

@router.get("/")
async def relaxation_root():
    """
    Root endpoint for relaxation API.
    
    Returns:
        dict: Available relaxation techniques
    """
    return {
        "status": "ok",
        "message": "Relaxation API is available",
        "techniques": [
            "breathing",
            "meditation",
            "stretching"
        ]
    }

@router.get("/breathing")
async def breathing_exercises():
    """
    Get breathing exercise recommendations.
    
    Returns:
        dict: List of breathing exercises
    """
    return {
        "status": "ok",
        "exercises": [
            {
                "name": "4-7-8 Breathing",
                "description": "Inhale for 4 seconds, hold for 7 seconds, exhale for 8 seconds",
                "duration": "5 minutes"
            },
            {
                "name": "Box Breathing",
                "description": "Inhale for 4 seconds, hold for 4 seconds, exhale for 4 seconds, hold for 4 seconds",
                "duration": "5 minutes"
            }
        ]
    }

@router.get("/meditation")
async def meditation_exercises():
    """
    Get meditation exercise recommendations.
    
    Returns:
        dict: List of meditation exercises
    """
    return {
        "status": "ok",
        "exercises": [
            {
                "name": "Mindfulness Meditation",
                "description": "Focus on your breath and present moment",
                "duration": "10 minutes"
            },
            {
                "name": "Body Scan Meditation",
                "description": "Progressively scan through your body, noticing sensations",
                "duration": "15 minutes"
            }
        ]
    }

@router.get("/stretching")
async def stretching_exercises():
    """
    Get stretching exercise recommendations.
    
    Returns:
        dict: List of stretching exercises
    """
    return {
        "status": "ok",
        "exercises": [
            {
                "name": "Neck Stretches",
                "description": "Gently tilt your head to each side, holding for 30 seconds",
                "duration": "2 minutes"
            },
            {
                "name": "Shoulder Rolls",
                "description": "Roll your shoulders forward and backward in a circular motion",
                "duration": "1 minute"
            }
        ]
    } 