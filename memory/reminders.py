import json
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REMINDERS_PATH = os.path.join(BASE_DIR, "memory", "reminders.json")

def _load():
    if not os.path.exists(REMINDERS_PATH):
        return []
    with open(REMINDERS_PATH, "r") as f:
        return json.load(f)

def _save(reminders):
    with open(REMINDERS_PATH, "w") as f:
        json.dump(reminders, f, indent=2)

def add_reminder(text):
    reminders = _load()
    reminders.append(text)
    _save(reminders)

def get_reminders():
    return _load()
