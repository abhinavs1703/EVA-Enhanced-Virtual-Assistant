import tkinter as tk
from threading import Thread
from queue import Queue
import time
import pyttsx3

from speech.stt import listen
from speech.wake_word import wait_for_wake_word
from eva_core.preprocess import clean_command

from nlp.intent_model import get_intent
from skills.time_date import handle as time_handler
from skills.open_app import handle as app_handler
from skills.notes_reminders import (
    handle_add_note,
    handle_get_notes,
    handle_add_reminder,
    handle_get_reminders
)
from memory.memory import init_memory, set_memory, get_memory

# =========================
# 🔊 SPEECH SYSTEM
# =========================

speech_queue = Queue()

def speech_worker():
    engine = pyttsx3.init(driverName="sapi5")
    engine.setProperty("rate", 180)

    while True:
        text = speech_queue.get()
        if text is None:
            break
        engine.say(text)
        engine.runAndWait()

def speak(text):
    speech_queue.put(text)

# =========================
# 🧠 COMMAND PROCESSING
# =========================

def process_command(output_box):
    # Hard timeout protection is inside listen()
    command = listen()

    if not command:
        output_box.insert(tk.END, "EVA: I did not understand.\n")
        speak("I did not understand.")
        return

    command = clean_command(command)
    output_box.insert(tk.END, f"You: {command}\n")

    response = None

    # ⚡ FAST PATH
    if command == "time":
        response = time_handler("get_time")

    elif "date" in command or "day" in command:
        response = time_handler("get_date")

    elif command.startswith("open "):
        response = app_handler(command)

    else:
        intent = get_intent(command)

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
            response = f"Your name is {name}" if name else "I don't know your name yet"

        elif intent == "add_note":
            response = handle_add_note(command)

        elif intent == "get_notes":
            response = handle_get_notes()

        elif intent == "add_reminder":
            response = handle_add_reminder(command)

        elif intent == "get_reminders":
            response = handle_get_reminders()

        else:
            response = "Sorry, I cannot do that yet."

    output_box.insert(tk.END, f"EVA: {response}\n\n")
    speak(response)

# =========================
# 🎤 WAKE WORD LOOP (FIXED)
# =========================

def wake_loop(output_box):
    while True:
        # 1️⃣ Wait for wake word
        wait_for_wake_word()

        output_box.insert(tk.END, "🔔 EVA is listening...\n")
        speak("Yes?")

        # 2️⃣ Small delay to RELEASE microphone
        time.sleep(0.3)

        # 3️⃣ Process one command
        process_command(output_box)

        # 4️⃣ Cool-down to reset recognizer state
        time.sleep(0.5)

        output_box.insert(tk.END, "🟢 EVA sleeping... Say 'Hey EVA'\n")

# =========================
# 🖥️ UI
# =========================

def main():
    init_memory()

    root = tk.Tk()
    root.title("EVA - Enhanced Virtual Assistant")
    root.geometry("500x400")

    output_box = tk.Text(root, wrap=tk.WORD)
    output_box.pack(expand=True, fill=tk.BOTH)

    def start_eva():
        start_button.config(state=tk.DISABLED)
        Thread(target=wake_loop, args=(output_box,), daemon=True).start()

    start_button = tk.Button(
        root,
        text="🎤 Start EVA",
        command=start_eva,
        height=2
    )
    start_button.pack(fill=tk.X)

    output_box.insert(
        tk.END,
        "EVA: Hello! I am online. Say 'Hey EVA' anytime.\n"
    )

    # Start speech engine
    Thread(target=speech_worker, daemon=True).start()
    speak("Hello. I am online.")

    root.mainloop()

if __name__ == "__main__":
    main()
