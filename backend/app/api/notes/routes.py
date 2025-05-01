from fastapi import APIRouter, HTTPException
from typing import Dict, List, Any, Optional
from pydantic import BaseModel
import uuid
from datetime import datetime

router = APIRouter()

# In-memory database for notes (will be lost on restart)
notes_db = {}

class NoteCreate(BaseModel):
    title: str
    content: str
    tags: Optional[List[str]] = []

class NoteUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    tags: Optional[List[str]] = None

class Note(BaseModel):
    id: str
    title: str
    content: str
    tags: List[str]
    created_at: str
    updated_at: str

@router.get("/", response_model=List[Note])
async def get_notes():
    """
    Get all notes.
    
    Returns:
        List[Note]: List of all stored notes
    """
    return list(notes_db.values())

@router.post("/", response_model=Note)
async def create_note(note: NoteCreate):
    """
    Create a new note.
    
    Args:
        note: Note data to create
        
    Returns:
        Note: The created note
    """
    note_id = str(uuid.uuid4())
    timestamp = datetime.utcnow().isoformat()
    
    new_note = Note(
        id=note_id,
        title=note.title,
        content=note.content,
        tags=note.tags or [],
        created_at=timestamp,
        updated_at=timestamp
    )
    
    notes_db[note_id] = new_note.dict()
    return new_note

@router.get("/{note_id}", response_model=Note)
async def get_note(note_id: str):
    """
    Get a specific note by ID.
    
    Args:
        note_id: ID of the note to retrieve
        
    Returns:
        Note: The requested note
        
    Raises:
        HTTPException: If the note is not found
    """
    if note_id not in notes_db:
        raise HTTPException(status_code=404, detail="Note not found")
    
    return notes_db[note_id]

@router.put("/{note_id}", response_model=Note)
async def update_note(note_id: str, note_update: NoteUpdate):
    """
    Update a specific note.
    
    Args:
        note_id: ID of the note to update
        note_update: Note data to update
        
    Returns:
        Note: The updated note
        
    Raises:
        HTTPException: If the note is not found
    """
    if note_id not in notes_db:
        raise HTTPException(status_code=404, detail="Note not found")
    
    note = notes_db[note_id]
    
    if note_update.title is not None:
        note["title"] = note_update.title
    
    if note_update.content is not None:
        note["content"] = note_update.content
    
    if note_update.tags is not None:
        note["tags"] = note_update.tags
    
    note["updated_at"] = datetime.utcnow().isoformat()
    notes_db[note_id] = note
    
    return note

@router.delete("/{note_id}")
async def delete_note(note_id: str):
    """
    Delete a specific note.
    
    Args:
        note_id: ID of the note to delete
        
    Returns:
        dict: A success message
        
    Raises:
        HTTPException: If the note is not found
    """
    if note_id not in notes_db:
        raise HTTPException(status_code=404, detail="Note not found")
    
    del notes_db[note_id]
    
    return {"status": "ok", "message": "Note deleted successfully"} 