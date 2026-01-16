import json
import os

MEMORY_FILE = "backend/user_memory.json"

def load_memory():
    if not os.path.exists(MEMORY_FILE):
        return {}
    with open(MEMORY_FILE, "r") as f:
        return json.load(f)

def save_memory(data):
    with open(MEMORY_FILE, "w") as f:
        json.dump(data, f)

def set_value(key, value):
    memory = load_memory()
    memory[key] = value
    save_memory(memory)

def get_value(key):
    memory = load_memory()
    return memory.get(key)
