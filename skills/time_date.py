from datetime import datetime

def handle(intent):
    if intent == "get_time":
        return datetime.now().strftime("The time is %I:%M %p")

    if intent == "get_date":
        return datetime.now().strftime("Today is %A, %d %B %Y")

    return None
