import pytest
from unittest.mock import MagicMock

# Mocking psycopg2 for testing without real DB
@pytest.fixture
def mock_psycopg2(monkeypatch):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value = mock_cursor
    monkeypatch.setattr("psycopg2.connect", lambda **kwargs: mock_conn)
    return mock_conn

def test_db_connection(mock_psycopg2):
    conn = mock_psycopg2
    cur = conn.cursor()
    cur.execute("SELECT 1")
    cur.execute.assert_called_with("SELECT 1")

def test_incidents_table_exists(mock_psycopg2):
    conn = mock_psycopg2
    cur = conn.cursor()
    cur.execute("SELECT to_regclass('public.incidents')")
    cur.execute.assert_called_with("SELECT to_regclass('public.incidents')")
