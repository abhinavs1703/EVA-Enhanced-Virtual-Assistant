import json
import os

NOTES_FILE = "backend/notes.json"

def load_notes():
    if not os.path.exists(NOTES_FILE):
        return []
    with open(NOTES_FILE, "r") as f:
        return json.load(f)

def save_notes(notes):
    with open(NOTES_FILE, "w") as f:
        json.dump(notes, f)

def add_note(text: str):
    notes = load_notes()
    notes.append(text)
    save_notes(notes)

def get_notes():
    return load_notes()
