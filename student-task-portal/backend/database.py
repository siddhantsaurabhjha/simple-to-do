import sqlite3
import os

# Define database file path in the same backend folder
DB_FILE = os.path.join(os.path.dirname(__file__), "database.db")

def get_db_connection():
    """Connect to SQLite database and set row factory to return dictionary-like rows."""
    conn = sqlite3.connect(DB_FILE)
    # sqlite3.Row allows accessing columns by name (e.g., row['name'])
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initialize the database by creating the records table if it does not exist."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            roll_number TEXT NOT NULL,
            task TEXT NOT NULL,
            category TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT 'Pending',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)
    conn.commit()
    conn.close()

def get_all_records():
    """Fetch all records from database ordered by newest first."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM records ORDER BY id DESC;")
    rows = cursor.fetchall()
    conn.close()
    # Convert sqlite3.Row objects into python dictionaries for JSON serialization
    return [dict(row) for row in rows]

def get_record_by_id(record_id):
    """Fetch a single record by its ID."""
    conn = get_db_connection()
    cursor = conn.cursor()
    # Parameterized SQL query using '?' placeholder to prevent SQL injection
    cursor.execute("SELECT * FROM records WHERE id = ?;", (record_id,))
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else None

def add_record(name, roll_number, task, category, status="Pending"):
    """Insert a new record into the database."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO records (name, roll_number, task, category, status)
        VALUES (?, ?, ?, ?, ?);
        """,
        (name, roll_number, task, category, status)
    )
    conn.commit()
    new_id = cursor.lastrowid
    conn.close()
    return get_record_by_id(new_id)

def update_record(record_id, name, roll_number, task, category, status):
    """Update existing record details in the database."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        UPDATE records
        SET name = ?, roll_number = ?, task = ?, category = ?, status = ?
        WHERE id = ?;
        """,
        (name, roll_number, task, category, status, record_id)
    )
    conn.commit()
    conn.close()
    return get_record_by_id(record_id)

def delete_record(record_id):
    """Delete a record from the database by ID."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM records WHERE id = ?;", (record_id,))
    conn.commit()
    deleted_count = cursor.rowcount
    conn.close()
    return deleted_count > 0
