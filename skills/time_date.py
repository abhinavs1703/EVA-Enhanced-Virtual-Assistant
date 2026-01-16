from datetime import datetime

def handle(intent: str) -> str:
    now = datetime.now()

    if intent == "get_time":
        hour = now.hour % 12
        hour = hour if hour != 0 else 12
        minute = f"{now.minute:02d}"
        period = "AM" if now.hour < 12 else "PM"
        return f"The time is {hour}:{minute} {period}"

    elif intent == "get_date":
        return now.strftime("Today is %A, %d %B %Y")

    else:
        return "I cannot get that information."
