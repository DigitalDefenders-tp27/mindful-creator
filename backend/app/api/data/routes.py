from fastapi import APIRouter, Response, HTTPException
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
    return [dict(zip(columns, row)) for row in rows]

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

@router.get("/emotion_distribution")
async def get_emotion_distribution():
    try:
        conn = get_connection()
    except Exception as e:
        # better feedback if connection fails
        raise HTTPException(status_code=500, detail=f"DB connection error: {e}")

    try:
        cur = conn.cursor()
        query = """
            SELECT 
                CASE 
                    WHEN daily_usage_time_minutes < 60 THEN 'Below 1h'
                    WHEN daily_usage_time_minutes BETWEEN 60 AND 180 THEN '1-3h'
                    WHEN daily_usage_time_minutes > 180 THEN '3-5h'
                END AS screen_time_group,
                dominant_emotion,
                COUNT(*)::float
                     / SUM(COUNT(*)) OVER (PARTITION BY 
                         CASE 
                             WHEN daily_usage_time_minutes < 60 THEN 'Below 1h'
                             WHEN daily_usage_time_minutes BETWEEN 60 AND 180 THEN '1-3h'
                             WHEN daily_usage_time_minutes > 180 THEN '3-5h'
                         END
                     ) * 100 AS percentage
            FROM train_cleaned
            WHERE daily_usage_time_minutes IS NOT NULL
              AND dominant_emotion IS NOT NULL
            GROUP BY screen_time_group, dominant_emotion
            ORDER BY screen_time_group, dominant_emotion;
        """
        cur.execute(query)
        rows = cur.fetchall()
        columns = [desc[0] for desc in cur.description]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Query error: {e}")
    finally:
        cur.close()
        conn.close()

    # send JSON back
    data = [dict(zip(columns, row)) for row in rows]
    return Response(content=json.dumps(data), media_type="application/json")
