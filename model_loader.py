"""
utils/model_loader.py
---------------------
Loads the best-trained model and vectorizer saved by train_model.py.

Reads model_info.json to know which model type won the MLflow comparison,
then loads model.pkl + vectorizer.pkl for use in the Flask app.
"""

import os
import json
import joblib

# ── Paths (relative to project root) ─────────────────────────────────────────
_BASE = os.path.dirname(os.path.dirname(__file__))   # project root
_MODELS_DIR = os.path.join(_BASE, "models")
_MODEL_PATH = os.path.join(_MODELS_DIR, "model.pkl")
_VECTORIZER_PATH = os.path.join(_MODELS_DIR, "vectorizer.pkl")
_MODEL_INFO_PATH = os.path.join(_MODELS_DIR, "model_info.json")

# ── Module-level cache (loaded once per process) ───────────────────────────
_model = None
_vectorizer = None
_model_info = None


def _load():
    """Load model and vectorizer from disk (called lazily on first use)."""
    global _model, _vectorizer, _model_info

    if not os.path.exists(_MODEL_PATH):
        raise FileNotFoundError(
            f"Model not found at '{_MODEL_PATH}'. "
            "Please run  'python train_model.py'  first."
        )
    if not os.path.exists(_VECTORIZER_PATH):
        raise FileNotFoundError(
            f"Vectorizer not found at '{_VECTORIZER_PATH}'. "
            "Please run  'python train_model.py'  first."
        )

    _model = joblib.load(_MODEL_PATH)
    _vectorizer = joblib.load(_VECTORIZER_PATH)

    if os.path.exists(_MODEL_INFO_PATH):
        with open(_MODEL_INFO_PATH) as f:
            _model_info = json.load(f)
    else:
        _model_info = {"model_type": "Unknown"}


def get_model_info() -> dict:
    """Return the metadata dict from model_info.json (model type, accuracy, …)."""
    if _model_info is None:
        _load()
    return _model_info


def predict_resume(resume_text: str) -> dict:
    """
    Predict the job category for a single resume text string.

    Parameters
    ----------
    resume_text : str
        Raw (un-cleaned) resume text extracted from a PDF.

    Returns
    -------
    dict with keys:
        category   – predicted label (str)
        confidence – probability of the predicted class (float 0-1)
        all_scores – {label: probability} for every class (dict)
        model_type – which model produced the result (str)
    """
    if _model is None:
        _load()

    # Transform using the trained vectorizer
    X = _vectorizer.transform([resume_text])

    # Predict
    predicted_label = _model.predict(X)[0]

    # Probability scores (if the model supports predict_proba)
    if hasattr(_model, "predict_proba"):
        proba = _model.predict_proba(X)[0]
        all_scores = dict(zip(_model.classes_, proba.tolist()))
        confidence = float(max(proba))
    else:
        # Fallback for models without predict_proba (e.g. LinearSVC)
        all_scores = {predicted_label: 1.0}
        confidence = 1.0

    return {
        "category": predicted_label,
        "confidence": confidence,
        "all_scores": all_scores,
        "model_type": _model_info.get("model_type", "Unknown") if _model_info else "Unknown",
    }
