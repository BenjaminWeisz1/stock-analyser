import sqlite3
from pathlib import Path

# Import the schemas from schemas.py
from .schemas import CREATE_USERS_TABLE, CREATE_STOCK_CACHE_TABLE

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
    cursor.execute(CREATE_STOCK_CACHE_TABLE)

    # Save changes
    conn.commit()

    # Close the connection
    conn.close()

def get_cached_stock(symbol: str, date: str):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT price, returns, volume
        FROM stock_cache
        WHERE symbol = ? AND date = ?
        """,
        (symbol, date)
    )

    row = cursor.fetchone()
    conn.close()

    return row

def insert_cached_stock(symbol, date, price, returns, volume):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT OR IGNORE INTO stock_cache
        (symbol, date, price, returns, volume)
        VALUES (?, ?, ?, ?, ?)
        """,
        (symbol, date, price, returns, volume)
    )
    conn.commit()
    conn.close()