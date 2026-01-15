def clean_command(text):
    text = text.lower().strip()

    fillers = [
        "please",
        "can you",
        "could you",
        "hey eva",
        "eva"
    ]

    for filler in fillers:
        text = text.replace(filler, "")

    return text.strip()
