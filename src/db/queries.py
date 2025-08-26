# src/db/queries.py
from typing import Optional, List, Dict, Any
from src.db.db import get_connection

# ---------- Users ----------

def create_user(username: str, password_hash: str) -> Dict[str, Any]:
    sql = """
        INSERT INTO users (username, password_hash)
        VALUES (%s, %s)
        RETURNING id, username, created_at;
    """
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(sql, (username, password_hash))
            row = cur.fetchone()
        conn.commit()
        return row
    finally:
        conn.close()

def get_user_by_username(username: str) -> Optional[Dict[str, Any]]:
    sql = "SELECT id, username, password_hash FROM users WHERE username = %s;"
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(sql, (username,))
            row = cur.fetchone()
        return row
    finally:
        conn.close()

# ---------- Incidents ----------

def insert_incident(incident_id: str, description: str, category: Optional[str]) -> Dict[str, Any]:
    """
    Upsert by incident_id to avoid dupes; update description/category if same id arrives.
    """
    sql = """
    INSERT INTO incidents (incident_id, description, category)
    VALUES (%s, %s, %s)
    ON CONFLICT (incident_id)
    DO UPDATE SET
        description = EXCLUDED.description,
        category = EXCLUDED.category
    RETURNING id, incident_id, description, category, received_at;
    """
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(sql, (incident_id, description, category))
            row = cur.fetchone()
        conn.commit()
        return row
    finally:
        conn.close()

def get_incidents(limit: int = 100, offset: int = 0) -> List[Dict[str, Any]]:
    sql = """
    SELECT id, incident_id, description, category, received_at
    FROM incidents
    ORDER BY received_at DESC
    LIMIT %s OFFSET %s;
    """
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(sql, (limit, offset))
            rows = cur.fetchall()
        return rows
    finally:
        conn.close()
