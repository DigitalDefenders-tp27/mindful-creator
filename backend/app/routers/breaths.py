from fastapi import APIRouter, HTTPException
from typing import List, Dict, Any
import random
import os
import json

router = APIRouter(
    prefix="/breaths",
    tags=["breaths"],
)

# Path to the breathing exercises data file
BREATHING_FILE = os.path.join("data", "breathing_exercises.json")

# Default breathing exercises in case the file doesn't exist
DEFAULT_BREATHING = [
    {
        "id": 1,
        "name": "Box Breathing",
        "description": "Inhale for 4 counts, hold for 4 counts, exhale for 4 counts, hold for 4 counts.",
        "duration": 4,
        "steps": [
            {"type": "inhale", "duration": 4, "message": "Inhale slowly through your nose"},
            {"type": "hold", "duration": 4, "message": "Hold your breath"},
            {"type": "exhale", "duration": 4, "message": "Exhale slowly through your mouth"},
            {"type": "hold", "duration": 4, "message": "Hold your breath"}
        ]
    },
    {
        "id": 2,
        "name": "4-7-8 Breathing",
        "description": "Inhale for 4 counts, hold for 7 counts, exhale for 8 counts.",
        "duration": 19,
        "steps": [
            {"type": "inhale", "duration": 4, "message": "Inhale quietly through your nose"},
            {"type": "hold", "duration": 7, "message": "Hold your breath"},
            {"type": "exhale", "duration": 8, "message": "Exhale completely through your mouth"}
        ]
    },
    {
        "id": 3,
        "name": "Diaphragmatic Breathing",
        "description": "Deep breathing technique that engages the diaphragm.",
        "duration": 8,
        "steps": [
            {"type": "inhale", "duration": 4, "message": "Inhale deeply through your nose, feel your abdomen expand"},
            {"type": "exhale", "duration": 4, "message": "Exhale slowly through your mouth, feel your abdomen contract"}
        ]
    }
]

def get_breathing_exercises() -> List[Dict[str, Any]]:
    """Load breathing exercises from the JSON file, or return defaults if file doesn't exist"""
    try:
        if os.path.exists(BREATHING_FILE):
            with open(BREATHING_FILE, 'r') as f:
                data = json.load(f)
                return data.get("exercises", DEFAULT_BREATHING)
        return DEFAULT_BREATHING
    except Exception as e:
        print(f"Error loading breathing exercises: {e}")
        return DEFAULT_BREATHING

@router.get("/")
async def get_all_exercises() -> Dict[str, List[Dict[str, Any]]]:
    """Get all available breathing exercises"""
    return {"exercises": get_breathing_exercises()}

@router.get("/{exercise_id}")
async def get_exercise(exercise_id: int) -> Dict[str, Any]:
    """Get a specific breathing exercise by ID"""
    exercises = get_breathing_exercises()
    
    for exercise in exercises:
        if exercise["id"] == exercise_id:
            return exercise
    
    raise HTTPException(status_code=404, detail=f"Breathing exercise with ID {exercise_id} not found")

@router.get("/random")
async def get_random_exercise() -> Dict[str, Any]:
    """Get a random breathing exercise"""
    exercises = get_breathing_exercises()
    
    if not exercises:
        raise HTTPException(status_code=404, detail="No breathing exercises available")
    
    random_exercise = random.choice(exercises)
    return random_exercise 