import speech_recognition as sr

WAKE_WORDS = ["hey eva", "eva"]

def wait_for_wake_word():
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source, duration=0.5)
        print("🟢 EVA sleeping... Say 'Hey EVA'")

        while True:
            try:
                audio = recognizer.listen(source, phrase_time_limit=3)
                text = recognizer.recognize_google(audio).lower()
                print("Heard:", text)

                for wake in WAKE_WORDS:
                    if wake in text:
                        print("🔵 Wake word detected")
                        return

            except sr.UnknownValueError:
                pass
            except sr.RequestError:
                pass
