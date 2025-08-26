# src/db/db.py
import os
import psycopg2
from psycopg2.extras import RealDictCursor

def get_connection():
    """
    Returns a new psycopg2 connection using env vars.
    Works with your docker-compose Postgres.
    """
    host = os.getenv("POSTGRES_HOST", "localhost")
    port = int(os.getenv("POSTGRES_PORT", "5432"))
    user = os.getenv("POSTGRES_USER", "admin")
    password = os.getenv("POSTGRES_PASSWORD", "admin")
    dbname = os.getenv("POSTGRES_DB", "incidentdb")

    return psycopg2.connect(
        host=host,
        port=port,
        user=user,
        password=password,
        dbname=dbname,
        cursor_factory=RealDictCursor,
    )
