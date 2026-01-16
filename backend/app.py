from fastapi import FastAPI
from pydantic import BaseModel

from nlp.intent_model import get_intent
from skills.time_date import handle as time_handler
from skills.app_control import open_app

from memory.memory import (
    init_memory,
    set_memory,
    get_memory,
    add_note,
    get_notes,
    add_reminder,
    get_all_reminders
)

# =========================
# 🚀 APP INIT
# =========================

app = FastAPI(title="EVA Backend")
init_memory()

# =========================
# 📦 MODELS
# =========================

class UserInput(BaseModel):
    command: str


class EvaResponse(BaseModel):
    intent: str
    response: str


# =========================
# 🧠 CORE LOGIC
# =========================

@app.post("/process", response_model=EvaResponse)
def process_command(data: UserInput):
    text = data.command.lower().strip()

    intent, confidence = get_intent(text)

    # 🔒 CONFIDENCE GATE
    if confidence < 0.2:
        return EvaResponse(
            intent="unknown",
            response="Sorry, I am not sure I understood that."
        )

    # ⏰ TIME
    if intent == "get_time":
        return EvaResponse(
            intent=intent,
            response=time_handler("get_time")
        )

    # 📅 DATE
    if intent == "get_date":
        return EvaResponse(
            intent=intent,
            response=time_handler("get_date")
        )

    # 👤 SET NAME
    if intent == "set_name":
        name = (
            text.replace("my name is", "")
                .replace("call me", "")
                .replace("i am called", "")
                .strip()
        )

        if not name:
            return EvaResponse(
                intent=intent,
                response="What should I call you?"
            )

        set_memory("user_name", name)
        return EvaResponse(
            intent=intent,
            response=f"Nice to meet you, {name}"
        )

    # 👤 GET NAME
    if intent == "get_name":
        name = get_memory("user_name")
        response = (
            f"Your name is {name}"
            if name else
            "I don't know your name yet."
        )
        return EvaResponse(intent=intent, response=response)

    # 📝 ADD NOTE
    if intent == "add_note":
        note_text = (
            text.replace("take a note", "")
                .replace("add a note", "")
                .replace("remember this", "")
                .strip()
        )

        if not note_text:
            return EvaResponse(
                intent=intent,
                response="What would you like me to note?"
            )

        add_note(note_text)
        return EvaResponse(
            intent=intent,
            response="Note saved."
        )

    # 📝 GET NOTES
    if intent == "get_notes":
        notes = get_notes()

        if not notes:
            response = "You don't have any notes yet."
        else:
            formatted = "\n".join(
                f"{i+1}. {n}" for i, n in enumerate(notes)
            )
            response = f"Your notes are:\n{formatted}"

        return EvaResponse(intent=intent, response=response)

    # ⏰ ADD REMINDER  ✅ FIXED
    if intent == "add_reminder":
        reminder_text = (
            text.replace("remind me", "")
                .replace("set a reminder", "")
                .strip()
        )

        if not reminder_text:
            return EvaResponse(
                intent=intent,
                response="What should I remind you about?"
            )

        add_reminder(reminder_text)
        return EvaResponse(
            intent=intent,
            response="Reminder saved."
        )

    # ⏰ GET REMINDERS  ✅ FIXED
    if intent == "get_reminders":
        reminders = get_all_reminders()

        if not reminders:
            response = "You have no reminders."
        else:
            formatted = "\n".join(
                f"{i+1}. {r}" for i, r in enumerate(reminders)
            )
            response = f"Your reminders are:\n{formatted}"

        return EvaResponse(intent=intent, response=response)

    # 🖥️ APP CONTROL (LAST)
    if intent == "open_app":
        return EvaResponse(
            intent=intent,
            response=open_app(text)
        )

    # ❓ FALLBACK
    return EvaResponse(
        intent=intent,
        response="Sorry, I cannot do that yet."
    )
