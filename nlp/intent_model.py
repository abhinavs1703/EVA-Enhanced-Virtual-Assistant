# nlp/intent_model.py

import json
import os
from typing import Tuple

import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

# =========================
# 📂 PATHS
# =========================

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INTENTS_PATH = os.path.join(BASE_DIR, "nlp", "intents.json")
MODEL_PATH = os.path.join(BASE_DIR, "nlp", "intent_model.pkl")

# =========================
# 🧠 GLOBAL MODEL CACHE
# =========================

_vectorizer = None
_model = None


# =========================
# 🔧 TRAIN MODEL
# =========================

def train_model() -> None:
    if not os.path.exists(INTENTS_PATH):
        raise FileNotFoundError("intents.json not found")

    with open(INTENTS_PATH, "r", encoding="utf-8") as f:
        intents = json.load(f)

    texts = []
    labels = []

    for intent, examples in intents.items():
        for example in examples:
            texts.append(example.lower().strip())
            labels.append(intent)

    if not texts:
        raise ValueError("No training data found in intents.json")

    vectorizer = TfidfVectorizer(
        ngram_range=(1, 2),
        stop_words="english",
        min_df=1
    )

    X = vectorizer.fit_transform(texts)

    model = LogisticRegression(
        max_iter=2000,
        class_weight="balanced"
    )

    model.fit(X, labels)

    joblib.dump((vectorizer, model), MODEL_PATH)

    print("✅ Intent model trained and saved")


# =========================
# 📦 LOAD MODEL (ONCE)
# =========================

def _load_model():
    global _vectorizer, _model

    if _vectorizer is not None and _model is not None:
        return

    if not os.path.exists(MODEL_PATH):
        train_model()

    _vectorizer, _model = joblib.load(MODEL_PATH)


# =========================
# 🧠 INTENT PREDICTION
# =========================

def get_intent(text: str) -> Tuple[str, float]:
    """
    Returns:
        (intent, confidence)
    """

    if not text or not text.strip():
        return "unknown", 0.0

    _load_model()

    cleaned = text.lower().strip()
    X = _vectorizer.transform([cleaned])

    probabilities = _model.predict_proba(X)[0]
    classes = _model.classes_

    best_index = probabilities.argmax()
    intent = classes[best_index]
    confidence = float(probabilities[best_index])

    # 🛡️ SAFETY GUARD AGAINST FALSE POSITIVES
    # Prevent open_app from hijacking unrelated commands
    if intent == "open_app":
        if not any(word in cleaned for word in ["open", "launch", "start"]):
            return "unknown", confidence * 0.4

    return intent, confidence
