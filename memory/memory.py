# memory/memory.py

import sqlite3
import os
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "eva_memory.db")


# =========================
# 🧠 INIT
# =========================

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
            created_at TEXT
        )
    """)

    conn.commit()
    conn.close()


# =========================
# 👤 USER MEMORY
# =========================

def set_memory(key: str, value: str):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute(
        "INSERT OR REPLACE INTO user_memory (key, value) VALUES (?, ?)",
        (key, value)
    )

    conn.commit()
    conn.close()


def get_memory(key: str):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute(
        "SELECT value FROM user_memory WHERE key = ?",
        (key,)
    )

    row = cursor.fetchone()
    conn.close()

    return row[0] if row else None


# =========================
# 📝 NOTES
# =========================

def add_note(content: str):
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

    cursor.execute(
        "SELECT content FROM notes ORDER BY id DESC"
    )

    notes = [row[0] for row in cursor.fetchall()]
    conn.close()

    return notes


# =========================
# ⏰ REMINDERS (TEXT ONLY)
# =========================

def add_reminder(content: str):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO reminders (content, created_at) VALUES (?, ?)",
        (content, datetime.now().isoformat())
    )

    conn.commit()
    conn.close()


def get_all_reminders():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute(
        "SELECT content FROM reminders ORDER BY id DESC"
    )

    reminders = [row[0] for row in cursor.fetchall()]
    conn.close()

    return reminders
