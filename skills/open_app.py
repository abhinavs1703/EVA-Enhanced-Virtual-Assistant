import subprocess

APP_PATHS = {
    "chrome": r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    "edge": r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
    "notepad": "notepad.exe",
    "calculator": "calc.exe"
}

def handle(command_text):
    for app, path in APP_PATHS.items():
        if app in command_text.lower():
            subprocess.Popen(path)
            return f"Opening {app}"

    return None
	