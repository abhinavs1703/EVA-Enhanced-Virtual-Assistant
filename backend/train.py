import json
import pickle
from pathlib import Path

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline


BASE_DIR = Path(__file__).resolve().parent
INTENTS_PATH = BASE_DIR / "intents.json"
MODEL_DIR = BASE_DIR / "models"
MODEL_PATH = MODEL_DIR / "intent_model.pkl"


def load_training_data():
    with open(INTENTS_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    texts = []
    labels = []

    for intent in data["intents"]:
        intent_name = intent["intent"]
        for example in intent["examples"]:
            texts.append(example)
            labels.append(intent_name)

    return texts, labels


def train_model(texts, labels):
    pipeline = Pipeline(
        [
            ("tfidf", TfidfVectorizer(
                ngram_range=(1, 2),
                stop_words="english"
            )),
            ("clf", LogisticRegression(
                max_iter=1000,
                solver="lbfgs",
                multi_class="auto"
            ))
        ]
    )

    pipeline.fit(texts, labels)
    return pipeline


def save_model(model):
    MODEL_DIR.mkdir(exist_ok=True)

    with open(MODEL_PATH, "wb") as f:
        pickle.dump(model, f)


def main():
    print("📚 Loading training data...")
    texts, labels = load_training_data()

    print(f"🧠 Training model on {len(texts)} examples...")
    model = train_model(texts, labels)

    print("💾 Saving model...")
    save_model(model)

    print("✅ Training complete!")
    print(f"📦 Model saved at: {MODEL_PATH}")


if __name__ == "__main__":
    main()
