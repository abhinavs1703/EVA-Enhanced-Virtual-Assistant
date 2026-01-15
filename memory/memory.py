import sqlite3
import os
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(__file__), "eva_memory.db")

def init_memory():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS user_memory (
            key TEXT PRIMARY KEY,
            value TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS notes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            content TEXT,
            created_at TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS reminders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            content TEXT,
            remind_at TEXT
        )
    """)

    conn.commit()
    conn.close()

def set_memory(key, value):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT OR REPLACE INTO user_memory (key, value) VALUES (?, ?)",
        (key, value)
    )
    conn.commit()
    conn.close()

def get_memory(key):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT value FROM user_memory WHERE key = ?",
        (key,)
    )
    row = cursor.fetchone()
    conn.close()
    return row[0] if row else None

# 📝 NOTES
def add_note(content):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO notes (content, created_at) VALUES (?, ?)",
        (content, datetime.now().isoformat())
    )
    conn.commit()
    conn.close()

def get_notes():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT content FROM notes ORDER BY id DESC")
    notes = [row[0] for row in cursor.fetchall()]
    conn.close()
    return notes

# ⏰ REMINDERS
def add_reminder(content, remind_at):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO reminders (content, remind_at) VALUES (?, ?)",
        (content, remind_at)
    )
    conn.commit()
    conn.close()

def get_due_reminders(current_time):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id, content FROM reminders WHERE remind_at <= ?",
        (current_time,)
    )
    reminders = cursor.fetchall()

    cursor.execute(
        "DELETE FROM reminders WHERE remind_at <= ?",
        (current_time,)
    )

    conn.commit()
    conn.close()
    return reminders

def get_all_reminders():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT content, remind_at FROM reminders ORDER BY remind_at")
    reminders = cursor.fetchall()
    conn.close()
    return reminders

