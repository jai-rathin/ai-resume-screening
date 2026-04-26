"""
model_loader.py
---------------
Loads the trained ML model and TF-IDF vectorizer from disk,
and provides a simple predict_resume() function for the Flask app.
"""

import os
import re
import joblib
import nltk
from nltk.corpus import stopwords

# ── Download NLTK data (runs once) ───────────────────────────────────────────
nltk.download("stopwords", quiet=True)

# ── Paths to saved model files ───────────────────────────────────────────────
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "models", "model.pkl")
VECTORIZER_PATH = os.path.join(BASE_DIR, "models", "vectorizer.pkl")

# ── Load model and vectorizer into memory ────────────────────────────────────
_model = None
_vectorizer = None


def _load_model():
    """Load the model and vectorizer from disk (lazy loading)."""
    global _model, _vectorizer

    if not os.path.exists(MODEL_PATH):
        raise FileNotFoundError(
            f"Model file not found at '{MODEL_PATH}'. "
            "Please run 'python train_model.py' first to train the model."
        )

    if not os.path.exists(VECTORIZER_PATH):
        raise FileNotFoundError(
            f"Vectorizer file not found at '{VECTORIZER_PATH}'. "
            "Please run 'python train_model.py' first to train the model."
        )

    _model = joblib.load(MODEL_PATH)
    _vectorizer = joblib.load(VECTORIZER_PATH)
    print("[OK] ML model and vectorizer loaded successfully.")


def clean_text(text):
    """
    Clean resume text before prediction.
    Mirrors the same preprocessing used during training.
    """
    if not isinstance(text, str):
        return ""

    # Lowercase
    text = text.lower()

    # Remove URLs
    text = re.sub(r"http\S+|www\S+", "", text)

    # Remove special characters and numbers
    text = re.sub(r"[^a-z\s]", "", text)

    # Remove extra whitespace
    text = re.sub(r"\s+", " ", text).strip()

    # Remove stopwords
    stop_words = set(stopwords.words("english"))
    words = text.split()
    words = [word for word in words if word not in stop_words]

    return " ".join(words)


def predict_resume(text):
    """
    Predict the job category for a given resume text.

    Args:
        text (str): Raw text extracted from a resume PDF.

    Returns:
        dict: {
            "category": str      — Predicted job category,
            "confidence": float  — Confidence score (0.0 to 1.0),
            "all_scores": dict   — All categories with their probabilities
        }
    """
    global _model, _vectorizer

    # Load model on first call
    if _model is None or _vectorizer is None:
        _load_model()

    # Clean the text the same way we cleaned training data
    cleaned = clean_text(text)

    if not cleaned:
        return {
            "category": "Unknown",
            "confidence": 0.0,
            "all_scores": {},
        }

    # Transform text to TF-IDF features
    features = _vectorizer.transform([cleaned])

    # Predict category
    predicted_category = _model.predict(features)[0]

    # Get probability scores for all categories
    probabilities = _model.predict_proba(features)[0]
    categories = _model.classes_

    # Build a dict of category → probability (sorted by probability)
    all_scores = dict(zip(categories, probabilities))
    all_scores = dict(sorted(all_scores.items(), key=lambda x: x[1], reverse=True))

    # Confidence is the probability of the predicted category
    confidence = max(probabilities)

    return {
        "category": predicted_category,
        "confidence": round(confidence, 4),
        "all_scores": {k: round(v, 4) for k, v in list(all_scores.items())[:5]},
    }
