import json
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INTENTS_PATH = os.path.join(BASE_DIR, "nlp", "intents.json")

with open(INTENTS_PATH, "r") as f:
    INTENTS = json.load(f)

def get_intent(text):
    text = text.lower()

    for intent, keywords in INTENTS.items():
        for keyword in keywords:
            if keyword in text:
                return intent

    return "unknown"
