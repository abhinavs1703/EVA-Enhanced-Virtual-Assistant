import os
import subprocess
import webbrowser
import shutil
import platform


def _open_browser():
    """
    Open the user's preferred browser.
    Priority:
    1. Brave
    2. Chrome
    3. Edge
    4. Default system browser
    """
    browsers = [
        ("brave", "brave.exe"),
        ("chrome", "chrome.exe"),
        ("edge", "msedge.exe"),
        ("firefox", "firefox.exe")
    ]

    for name, exe in browsers:
        path = shutil.which(exe)
        if path:
            subprocess.Popen([path])
            return f"Opening {name.capitalize()} browser."

    # Fallback to system default
    webbrowser.open("https://www.google.com")
    return "Opening your default browser."


def open_app(text: str) -> str:
    text = text.lower()

    if "browser" in text or "internet" in text:
        return _open_browser()

    if "calculator" in text:
        subprocess.Popen("calc")
        return "Opening Calculator."

    if "notepad" in text:
        subprocess.Popen("notepad")
        return "Opening Notepad."

    if "settings" in text:
        subprocess.Popen("ms-settings:")
        return "Opening Settings."

    return "Which app should I open?"
