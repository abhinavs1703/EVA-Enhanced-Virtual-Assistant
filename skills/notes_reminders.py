from memory.memory import add_note, get_notes, add_reminder
from datetime import datetime
import re
from memory.memory import get_all_reminders

def handle_get_reminders():
    reminders = get_all_reminders()
    if not reminders:
        return "You have no reminders."

    response = "Your reminders are: "
    for r in reminders[:5]:
        response += r[0] + ", "
    return response


def handle_add_note(command):
    # Remove trigger phrases
    triggers = ["take a note", "add note", "remember this"]
    content = command

    for t in triggers:
        content = content.replace(t, "")

    content = content.replace("to", "").strip()

    if not content:
        return "What should I note down?"

    add_note(content)
    return f"Note saved: {content}"

def handle_get_notes():
    notes = get_notes()
    if not notes:
        return "You have no notes."
    return "Your notes are: " + "; ".join(notes[:5])

def handle_add_reminder(command):
    # Expected format: remind me to <task> at <time>
    try:
        # Extract time using regex (very tolerant)
        time_match = re.search(r'at\s+(.+)', command)
        if not time_match:
            return "Please specify a time."

        time_text = time_match.group(1)
        task = command.split("remind me to")[1].split("at")[0].strip()

        # Normalize time text
        time_text = time_text.replace(".", "").replace("p m", "pm").replace("a m", "am")

        remind_time = datetime.strptime(time_text, "%I:%M %p")
        now = datetime.now()
        remind_at = now.replace(
            hour=remind_time.hour,
            minute=remind_time.minute,
            second=0
        )

        add_reminder(task, remind_at.isoformat())
        return f"Reminder set to {task} at {time_text}"

    except Exception as e:
        print("Reminder parsing error:", e)
        return "Sorry, I couldn't understand the reminder time."
