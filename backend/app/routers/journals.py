from fastapi import APIRouter, HTTPException, Body
from typing import List, Dict, Any, Optional
from datetime import datetime
import os
import json
import uuid

router = APIRouter(
    prefix="/journals",
    tags=["journals"],
)

# Path to the journal entries data file
JOURNALS_DIR = os.path.join("data", "journals")
JOURNALS_FILE = os.path.join(JOURNALS_DIR, "entries.json")

# Ensure the journals directory exists
os.makedirs(JOURNALS_DIR, exist_ok=True)

def get_journal_entries() -> List[Dict[str, Any]]:
    """Load journal entries from the JSON file, or return an empty list if file doesn't exist"""
    try:
        if os.path.exists(JOURNALS_FILE):
            with open(JOURNALS_FILE, 'r') as f:
                data = json.load(f)
                return data.get("entries", [])
        return []
    except Exception as e:
        print(f"Error loading journal entries: {e}")
        return []

def save_journal_entries(entries: List[Dict[str, Any]]) -> bool:
    """Save journal entries to the JSON file"""
    try:
        # Ensure the directory exists
        os.makedirs(os.path.dirname(JOURNALS_FILE), exist_ok=True)
        
        # Save the entries
        with open(JOURNALS_FILE, 'w') as f:
            json.dump({"entries": entries}, f, indent=2)
        return True
    except Exception as e:
        print(f"Error saving journal entries: {e}")
        return False

@router.get("/")
async def get_all_entries() -> Dict[str, List[Dict[str, Any]]]:
    """Get all journal entries"""
    return {"entries": get_journal_entries()}

@router.get("/{entry_id}")
async def get_entry(entry_id: str) -> Dict[str, Any]:
    """Get a specific journal entry by ID"""
    entries = get_journal_entries()
    
    for entry in entries:
        if entry["id"] == entry_id:
            return entry
    
    raise HTTPException(status_code=404, detail=f"Journal entry with ID {entry_id} not found")

@router.post("/")
async def create_entry(
    content: str = Body(..., embed=True),
    mood: Optional[str] = Body(None, embed=True),
    tags: Optional[List[str]] = Body(None, embed=True)
) -> Dict[str, Any]:
    """Create a new journal entry"""
    entries = get_journal_entries()
    
    # Create a new entry
    new_entry = {
        "id": str(uuid.uuid4()),
        "content": content,
        "mood": mood or "neutral",
        "tags": tags or [],
        "created_at": datetime.now().isoformat(),
        "updated_at": datetime.now().isoformat()
    }
    
    # Add to the list of entries
    entries.append(new_entry)
    
    # Save the updated entries
    if not save_journal_entries(entries):
        raise HTTPException(status_code=500, detail="Failed to save journal entry")
    
    return new_entry

@router.put("/{entry_id}")
async def update_entry(
    entry_id: str,
    content: Optional[str] = Body(None, embed=True),
    mood: Optional[str] = Body(None, embed=True),
    tags: Optional[List[str]] = Body(None, embed=True)
) -> Dict[str, Any]:
    """Update an existing journal entry"""
    entries = get_journal_entries()
    
    # Find the entry to update
    for i, entry in enumerate(entries):
        if entry["id"] == entry_id:
            # Update the fields
            if content is not None:
                entry["content"] = content
            if mood is not None:
                entry["mood"] = mood
            if tags is not None:
                entry["tags"] = tags
            
            entry["updated_at"] = datetime.now().isoformat()
            
            # Save the updated entries
            if not save_journal_entries(entries):
                raise HTTPException(status_code=500, detail="Failed to save journal entry")
            
            return entry
    
    raise HTTPException(status_code=404, detail=f"Journal entry with ID {entry_id} not found")

@router.delete("/{entry_id}")
async def delete_entry(entry_id: str) -> Dict[str, bool]:
    """Delete a journal entry"""
    entries = get_journal_entries()
    
    # Find the entry to delete
    for i, entry in enumerate(entries):
        if entry["id"] == entry_id:
            # Remove the entry
            entries.pop(i)
            
            # Save the updated entries
            if not save_journal_entries(entries):
                raise HTTPException(status_code=500, detail="Failed to delete journal entry")
            
            return {"success": True}
    
    raise HTTPException(status_code=404, detail=f"Journal entry with ID {entry_id} not found") 