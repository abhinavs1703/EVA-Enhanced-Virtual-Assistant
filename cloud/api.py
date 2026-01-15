import sys
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
from flask import Flask, request, jsonify
from nlp.intent_model import get_intent
from skills.time_date import handle as time_handler
from skills.notes_reminders import (
    handle_add_note,
    handle_get_notes,
    handle_add_reminder,
    handle_get_reminders
)
from memory.memory import init_memory, set_memory, get_memory

app = Flask(__name__)
init_memory()

@app.route("/process", methods=["POST"])
def process():
    data = request.json
    command = data.get("command", "").lower()

    intent = get_intent(command)
    response = "Sorry, I cannot do that yet."

    if intent in ["get_time", "get_date"]:
        response = time_handler(intent)

    elif intent == "add_note":
        response = handle_add_note(command)

    elif intent == "get_notes":
        response = handle_get_notes()

    elif intent == "add_reminder":
        response = handle_add_reminder(command)

    elif intent == "get_reminders":
        response = handle_get_reminders()

    elif intent == "set_name":
        name = command.replace("my name is", "").strip()
        set_memory("user_name", name)
        response = f"Nice to meet you, {name}"

    elif intent == "get_name":
        name = get_memory("user_name")
        response = f"Your name is {name}" if name else "I don't know your name yet"

    return jsonify({
        "intent": intent,
        "response": response
    })

if __name__ == "__main__":


    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

