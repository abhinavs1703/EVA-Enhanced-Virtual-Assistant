# skills/app_control.py

import os
import webbrowser
import subprocess
import sys

def open_app(text: str) -> str:
    text = text.lower()

    # =========================
    # 🌐 BROWSER (SMART)
    # =========================
    if "browser" in text or "internet" in text:
        try:
            webbrowser.open("https://www.google.com")
            return "Opening your browser."
        except Exception:
            return "I could not open the browser."

    # =========================
    # 🧮 CALCULATOR
    # =========================
    if "calculator" in text:
        try:
            if sys.platform.startswith("win"):
                subprocess.Popen("calc")
            elif sys.platform.startswith("darwin"):
                subprocess.Popen(["open", "-a", "Calculator"])
            else:
                subprocess.Popen(["gnome-calculator"])
            return "Opening calculator."
        except Exception:
            return "I could not open calculator."

    # =========================
    # 📝 NOTEPAD / TEXT EDITOR
    # =========================
    if "notepad" in text or "text editor" in text:
        try:
            if sys.platform.startswith("win"):
                subprocess.Popen("notepad")
            elif sys.platform.startswith("darwin"):
                subprocess.Popen(["open", "-a", "TextEdit"])
            else:
                subprocess.Popen(["gedit"])
            return "Opening text editor."
        except Exception:
            return "I could not open text editor."

    return "I don't know which app to open."
