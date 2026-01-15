from speech.stt import listen
import pyttsx3

from nlp.intent_model import get_intent
from eva_core.preprocess import clean_command

from skills.time_date import handle as time_handler
from skills.open_app import handle as app_handler

from memory.memory import init_memory, set_memory, get_memory
from skills.notes_reminders import (
    handle_add_note,
    handle_get_notes,
    handle_add_reminder
)


def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()


def main():
    init_memory()

    speak("EVA is online. How can I help you?")

    command = listen()
    if not command:
        speak("I did not understand.")
        return

    # 🧹 Clean command (speed + reliability)
    command = clean_command(command)
    print("Command:", command)

    response = None

    # ⚡ FAST COMMAND SHORT-CIRCUITS (NO NLP)
    if command == "time":
        response = time_handler("get_time")

    elif "date" in command or "day" in command:
        response = time_handler("get_date")

    elif command.startswith("open "):
        response = app_handler(command)

    else:
        # 🧠 NLP PATH (only if needed)
        intent = get_intent(command)
        print("Detected intent:", intent)

        if intent in ["get_time", "get_date"]:
            response = time_handler(intent)

        elif intent == "open_app":
            response = app_handler(command)

        elif intent == "set_name":
            name = command.replace("my name is", "").strip()
            set_memory("user_name", name)
            response = f"Nice to meet you, {name}"

        elif intent == "get_name":
            name = get_memory("user_name")
            response = (
                f"Your name is {name}"
                if name else
                "I don't know your name yet"
            )
        elif intent == "add_note":
            response = handle_add_note(command)
        elif intent == "get_notes":
            response = handle_get_notes()
        elif intent == "add_reminder":
            response = handle_add_reminder(command)


        else:
            response = "Sorry, I cannot do that yet."

    # 🔊 Output
    if response:
        speak(response)
    else:
        speak("Sorry, I cannot do that yet.")


if __name__ == "__main__":
    main()
