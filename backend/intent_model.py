import pickle
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
MODEL_PATH = BASE_DIR / "models" / "intent_model.pkl"


class IntentClassifier:
    def __init__(self):
        self.model = self._load_model()

    def _load_model(self):
        if not MODEL_PATH.exists():
            raise FileNotFoundError(
                "Intent model not found. Please run train.py first."
            )

        with open(MODEL_PATH, "rb") as f:
            return pickle.load(f)

    def predict(self, text: str, threshold: float = 0.4) -> str:
        """
        Predict intent for input text.
        Returns 'fallback' if confidence is low.
        """
        if not text or not text.strip():
            return "fallback"

        probs = self.model.predict_proba([text])[0]
        classes = self.model.classes_

        max_index = probs.argmax()
        confidence = probs[max_index]
        intent = classes[max_index]

        if confidence < threshold:
            return "fallback"

        return intent


# Singleton-style loader (load once, reuse everywhere)
intent_classifier = IntentClassifier()


def get_intent(text: str) -> str:
    return intent_classifier.predict(text)
