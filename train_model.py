"""
train_model.py
--------------
Trains TWO resume-category classifiers and tracks both with MLflow.

Models:
  1. Logistic Regression  (TF-IDF + LR)
  2. Random Forest        (TF-IDF + RF)

MLflow tracks every run's parameters, metrics, and artifacts.
The best model (by test accuracy) is saved to models/ and marked
as the production model in model_info.json.

Usage:
    python train_model.py

MLflow UI:
    mlflow ui          # visit http://127.0.0.1:5000
"""

import os
import re
import json
import pandas as pd
import nltk
from nltk.corpus import stopwords

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    accuracy_score,
    f1_score,
    classification_report,
)
import joblib
import mlflow
import mlflow.sklearn

# ── NLTK setup ────────────────────────────────────────────────────────────────
nltk.download("stopwords", quiet=True)

# ── MLflow experiment name ────────────────────────────────────────────────────
EXPERIMENT_NAME = "resume-screening"

# ── Output paths ──────────────────────────────────────────────────────────────
MODELS_DIR = os.path.join(os.path.dirname(__file__), "models")
MODEL_PATH = os.path.join(MODELS_DIR, "model.pkl")
VECTORIZER_PATH = os.path.join(MODELS_DIR, "vectorizer.pkl")
MODEL_INFO_PATH = os.path.join(MODELS_DIR, "model_info.json")


# ── Text Preprocessing ────────────────────────────────────────────────────────
def clean_text(text: str) -> str:
    """Lowercase, strip URLs/special chars, remove stopwords."""
    if not isinstance(text, str):
        return ""
    text = text.lower()
    text = re.sub(r"http\S+|www\S+", "", text)
    text = re.sub(r"[^a-z\s]", "", text)
    text = re.sub(r"\s+", " ", text).strip()
    stop_words = set(stopwords.words("english"))
    return " ".join(w for w in text.split() if w not in stop_words)


# ── Load & preprocess dataset ─────────────────────────────────────────────────
def load_data():
    csv_path = os.path.join("dataset", "Resume", "Resume.csv")
    print(f"\n[DATA] Loading dataset from '{csv_path}' ...")
    df = pd.read_csv(csv_path)
    print(f"       {len(df)} resumes | {df['Category'].nunique()} categories")

    print("[DATA] Cleaning text ...")
    df["cleaned"] = df["Resume_str"].apply(clean_text)
    df = df[df["cleaned"].str.len() > 0].reset_index(drop=True)
    print(f"       {len(df)} resumes after cleaning\n")
    return df


# ── TF-IDF vectorisation ──────────────────────────────────────────────────────
def vectorise(df, max_features: int = 5000):
    vectorizer = TfidfVectorizer(max_features=max_features)
    X = vectorizer.fit_transform(df["cleaned"])
    y = df["Category"]
    return X, y, vectorizer


# ── Train + log one model run ─────────────────────────────────────────────────
def train_and_log(
    model_name: str,
    model,
    X_train,
    X_test,
    y_train,
    y_test,
    vectorizer,
    extra_params: dict,
):
    """
    Fit `model`, compute metrics, log everything to MLflow,
    and return a results dict.
    """
    with mlflow.start_run(run_name=model_name):
        # ── log hyper-params ─────────────────────────────────────────────────
        mlflow.log_param("model_type", model_name)
        mlflow.log_param("tfidf_max_features", vectorizer.max_features)
        for k, v in extra_params.items():
            mlflow.log_param(k, v)

        # ── train ─────────────────────────────────────────────────────────────
        print(f"  [RUN] Training {model_name} ...")
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)

        # ── metrics ───────────────────────────────────────────────────────────
        accuracy = accuracy_score(y_test, y_pred)
        f1_macro = f1_score(y_test, y_pred, average="macro", zero_division=0)
        f1_weighted = f1_score(y_test, y_pred, average="weighted", zero_division=0)

        mlflow.log_metric("accuracy", accuracy)
        mlflow.log_metric("f1_macro", f1_macro)
        mlflow.log_metric("f1_weighted", f1_weighted)

        # ── log sklearn model artifact ────────────────────────────────────────
        mlflow.sklearn.log_model(model, artifact_path="model")

        # ── console report ────────────────────────────────────────────────────
        print(f"       Accuracy : {accuracy:.4f}")
        print(f"       F1 Macro : {f1_macro:.4f}")
        print(f"       F1 Weighted: {f1_weighted:.4f}")
        print(classification_report(y_test, y_pred, zero_division=0))

        run_id = mlflow.active_run().info.run_id

    return {
        "model_name": model_name,
        "model": model,
        "accuracy": accuracy,
        "f1_macro": f1_macro,
        "f1_weighted": f1_weighted,
        "run_id": run_id,
    }


# ── Main training pipeline ────────────────────────────────────────────────────
def train():
    os.makedirs(MODELS_DIR, exist_ok=True)

    # ── MLflow setup ──────────────────────────────────────────────────────────
    mlflow.set_experiment(EXPERIMENT_NAME)
    print(f"[MLFLOW] Experiment: '{EXPERIMENT_NAME}'")

    # ── Load data ─────────────────────────────────────────────────────────────
    df = load_data()
    MAX_FEATURES = 5000
    X, y, vectorizer = vectorise(df, max_features=MAX_FEATURES)

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    print(f"[SPLIT] Train: {X_train.shape[0]} | Test: {X_test.shape[0]}\n")

    # ── Model 1: Logistic Regression ──────────────────────────────────────────
    lr_params = {"C": 1.0, "max_iter": 1000, "solver": "lbfgs"}
    lr_result = train_and_log(
        model_name="LogisticRegression",
        model=LogisticRegression(
            C=lr_params["C"],
            max_iter=lr_params["max_iter"],
            solver=lr_params["solver"],
            random_state=42,
        ),
        X_train=X_train, X_test=X_test,
        y_train=y_train, y_test=y_test,
        vectorizer=vectorizer,
        extra_params=lr_params,
    )

    # ── Model 2: Random Forest ────────────────────────────────────────────────
    rf_params = {"n_estimators": 200, "max_depth": None, "min_samples_split": 2}
    rf_result = train_and_log(
        model_name="RandomForest",
        model=RandomForestClassifier(
            n_estimators=rf_params["n_estimators"],
            max_depth=rf_params["max_depth"],
            min_samples_split=rf_params["min_samples_split"],
            random_state=42,
            n_jobs=-1,
        ),
        X_train=X_train, X_test=X_test,
        y_train=y_train, y_test=y_test,
        vectorizer=vectorizer,
        extra_params=rf_params,
    )

    # ── Compare & pick best model ─────────────────────────────────────────────
    results = [lr_result, rf_result]
    best = max(results, key=lambda r: r["accuracy"])
    print("=" * 60)
    print(f"[COMPARE] Results summary:")
    for r in results:
        marker = "  ← BEST" if r is best else ""
        print(f"  {r['model_name']:25s}  acc={r['accuracy']:.4f}  "
              f"f1={r['f1_macro']:.4f}{marker}")
    print("=" * 60)
    print(f"\n[BEST]  {best['model_name']} with accuracy {best['accuracy']:.4f}")

    # ── Save best model + vectorizer ──────────────────────────────────────────
    joblib.dump(best["model"], MODEL_PATH)
    joblib.dump(vectorizer, VECTORIZER_PATH)

    model_info = {
        "model_type": best["model_name"],
        "accuracy": round(best["accuracy"], 6),
        "f1_macro": round(best["f1_macro"], 6),
        "f1_weighted": round(best["f1_weighted"], 6),
        "mlflow_run_id": best["run_id"],
        "mlflow_experiment": EXPERIMENT_NAME,
        "tfidf_max_features": MAX_FEATURES,
    }
    with open(MODEL_INFO_PATH, "w") as f:
        json.dump(model_info, f, indent=2)

    print(f"\n[SAVED] model.pkl       → {MODEL_PATH}")
    print(f"[SAVED] vectorizer.pkl  → {VECTORIZER_PATH}")
    print(f"[SAVED] model_info.json → {MODEL_INFO_PATH}")
    print("\n[DONE] Training complete! Run  'mlflow ui'  to explore results.\n")


# ── Entry point ───────────────────────────────────────────────────────────────
if __name__ == "__main__":
    train()
