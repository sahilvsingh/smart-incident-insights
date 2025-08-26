# src/db/setup.py
"""
Create required tables & indexes for the app (users, incidents).
Run:
  python -m src.db.setup
"""
from src.db.db import get_connection

DDL_STATEMENTS = [
    # users table
    """
    CREATE TABLE IF NOT EXISTS users (
        id SERIAL PRIMARY KEY,
        username TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL,
        created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
    );
    """,
    "CREATE UNIQUE INDEX IF NOT EXISTS idx_users_username ON users(username);",

    # incidents table (ML category stored)
    """
    CREATE TABLE IF NOT EXISTS incidents (
        id SERIAL PRIMARY KEY,
        incident_id TEXT NOT NULL,
        description TEXT NOT NULL,
        category TEXT,
        received_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
    );
    """,
    # Uniqueness so we can upsert on incident_id
    "CREATE UNIQUE INDEX IF NOT EXISTS ux_incidents_incident_id ON incidents(incident_id);",
    "CREATE INDEX IF NOT EXISTS idx_incidents_received_at ON incidents(received_at);",
]

def create_schema():
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            for ddl in DDL_STATEMENTS:
                cur.execute(ddl)
        conn.commit()
        print("✅ Database tables & indexes ready.")
    finally:
        conn.close()

if __name__ == "__main__":
    create_schema()
