"""
train_model.py
--------------
Trains a resume-category classifier using the Resume.csv dataset.

Steps:
    1. Load dataset from CSV
    2. Preprocess text (lowercase, remove stopwords & special characters)
    3. Convert text to TF-IDF features
    4. Train a Logistic Regression model
    5. Save model + vectorizer to the models/ folder

Usage:
    python train_model.py
"""

import os
import re
import pandas as pd
import nltk
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score
import joblib

# ── Download NLTK data (runs once) ───────────────────────────────────────────
nltk.download("stopwords", quiet=True)


# ── Text Preprocessing ──────────────────────────────────────────────────────
def clean_text(text):
    """
    Clean and preprocess a single resume text string.

    Steps:
        1. Convert to lowercase
        2. Remove URLs
        3. Remove special characters (keep only letters and spaces)
        4. Remove extra whitespace
        5. Remove English stopwords
    """
    if not isinstance(text, str):
        return ""

    # Lowercase
    text = text.lower()

    # Remove URLs
    text = re.sub(r"http\S+|www\S+", "", text)

    # Remove special characters and numbers (keep only letters and spaces)
    text = re.sub(r"[^a-z\s]", "", text)

    # Remove extra whitespace
    text = re.sub(r"\s+", " ", text).strip()

    # Remove stopwords
    stop_words = set(stopwords.words("english"))
    words = text.split()
    words = [word for word in words if word not in stop_words]

    return " ".join(words)


# ── Main Training Pipeline ──────────────────────────────────────────────────
def train():
    """Load data, preprocess, train model, and save to disk."""

    # ── Step 1: Load the dataset ─────────────────────────────────────────
    csv_path = os.path.join("dataset", "Resume", "Resume.csv")
    print(f"[1/5] Loading dataset from '{csv_path}' ...")

    df = pd.read_csv(csv_path)
    print(f"       Loaded {len(df)} resumes across {df['Category'].nunique()} categories.\n")

    # ── Step 2: Preprocess text ──────────────────────────────────────────
    print("[2/5] Preprocessing resume text ...")
    df["cleaned"] = df["Resume_str"].apply(clean_text)

    # Drop rows with empty cleaned text
    df = df[df["cleaned"].str.len() > 0]
    print(f"       {len(df)} resumes after cleaning.\n")

    # ── Step 3: TF-IDF Vectorization ─────────────────────────────────────
    print("[3/5] Building TF-IDF features ...")
    vectorizer = TfidfVectorizer(max_features=5000)
    X = vectorizer.fit_transform(df["cleaned"])
    y = df["Category"]
    print(f"       Feature matrix shape: {X.shape}\n")

    # ── Step 4: Train/Test Split & Model Training ────────────────────────
    print("[4/5] Training Logistic Regression model ...")
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    model = LogisticRegression(max_iter=1000, random_state=42)
    model.fit(X_train, y_train)

    # Evaluate on test set
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    print(f"       Test Accuracy: {accuracy:.2%}\n")
    print("       Classification Report:")
    print(classification_report(y_test, y_pred))

    # ── Step 5: Save model and vectorizer ────────────────────────────────
    models_dir = os.path.join(os.path.dirname(__file__), "models")
    os.makedirs(models_dir, exist_ok=True)

    model_path = os.path.join(models_dir, "model.pkl")
    vectorizer_path = os.path.join(models_dir, "vectorizer.pkl")

    joblib.dump(model, model_path)
    joblib.dump(vectorizer, vectorizer_path)

    print(f"[5/5] Model saved to '{model_path}'")
    print(f"       Vectorizer saved to '{vectorizer_path}'")
    print("\n[DONE] Training complete!")


# ── Entry Point ──────────────────────────────────────────────────────────────
if __name__ == "__main__":
    train()
