import sqlite3
from pathlib import Path

# Import the schema from schemas.py
from .schemas import CREATE_USERS_TABLE

# Path to SQLite database file
DB_PATH = Path(__file__).resolve().parent / "app.db"

def get_connection():
    conn = sqlite3.connect(DB_PATH)

    # Create a dictionary cursor to allow column access by name
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(CREATE_USERS_TABLE)

    # Save changes
    conn.commit()

    # Close the connection
    conn.close()