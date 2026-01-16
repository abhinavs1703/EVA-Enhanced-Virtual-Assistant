import re

def clean_command(text: str) -> str:
    """
    Cleans user speech input safely without breaking words.
    """

    if not text:
        return ""

    text = text.lower().strip()

    # Fillers / wake words (as whole words only)
    fillers = [
        "hey eva",
        "eva",
        "please",
        "can you",
        "could you"
    ]

    for filler in fillers:
        # Remove filler only if it appears as a phrase
        pattern = r"\b" + re.escape(filler) + r"\b"
        text = re.sub(pattern, "", text)

    # Normalize whitespace
    text = re.sub(r"\s+", " ", text)

    return text.strip()
