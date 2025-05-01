from fastapi import APIRouter, Response
from typing import List, Dict, Any
import json
from database import get_connection

router = APIRouter()

@router.get("/train_cleaned")
async def get_train_cleaned():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM train_cleaned")
    rows = cur.fetchall()
    columns = [desc[0] for desc in cur.description]
    cur.close()
    conn.close()
    
    data = [dict(zip(columns, row)) for row in rows]
    return Response(content=json.dumps(data), media_type="application/json")

@router.get("/smmh_cleaned")
async def get_smmh_cleaned():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM smmh_cleaned")
    rows = cur.fetchall()
    columns = [desc[0] for desc in cur.description]
    cur.close()
    conn.close()
    return [dict(zip(columns, row)) for row in rows]

@router.get("/screen_time_data")
async def get_screen_time_data():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM screen_time_data ORDER BY date")
    rows = cur.fetchall()
    columns = [desc[0] for desc in cur.description]
    cur.close()
    conn.close()
    return [dict(zip(columns, row)) for row in rows]

@router.get("/music_mental_health_data")
async def get_music_mental_health_data():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM music_mental_health_data")
    rows = cur.fetchall()
    columns = [desc[0] for desc in cur.description]
    cur.close()
    conn.close()
    return [dict(zip(columns, row)) for row in rows] 