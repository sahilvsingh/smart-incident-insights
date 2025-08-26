#!/usr/bin/env python3
import argparse
import os
import joblib
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report

MODEL_PATH = os.path.join(os.path.dirname(__file__), "incident_model.pkl")
VECTORIZER_PATH = os.path.join(os.path.dirname(__file__), "vectorizer.pkl")

def load_data(file_path: str) -> pd.DataFrame:
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Dataset not found: {file_path}")
    df = pd.read_csv(file_path)
    if df.empty:
        raise ValueError("Dataset is empty.")
    print(f"✅ Loaded dataset with shape: {df.shape}")
    return df

def _safe_test_size(y, test_size=0.2):
    n_samples = len(y)
    n_classes = len(set(y))
    min_test_size = n_classes / max(n_samples, 1)
    return max(test_size, min_test_size)

def train(data_path: str, test_size: float = 0.2, random_state: int = 42):
    df = load_data(data_path)
    X_text = df.iloc[:, 0].astype(str)
    y = df.iloc[:, 1].astype(str)

    test_size = _safe_test_size(y, test_size=test_size)

    X_train_text, X_test_text, y_train, y_test = train_test_split(
        X_text, y, test_size=test_size, stratify=y, random_state=random_state
    )

    vectorizer = TfidfVectorizer(ngram_range=(1, 2), min_df=1)
    X_train = vectorizer.fit_transform(X_train_text)

    model = LogisticRegression(max_iter=1000)
    model.fit(X_train, y_train)
    print("✅ Model training completed")

    X_test = vectorizer.transform(X_test_text)
    y_pred = model.predict(X_test)
    print("\n📊 Classification Report:\n")
    print(classification_report(y_test, y_pred))

    os.makedirs(os.path.dirname(MODEL_PATH), exist_ok=True)
    joblib.dump(model, MODEL_PATH)
    joblib.dump(vectorizer, VECTORIZER_PATH)
    print(f"💾 Model saved at: {MODEL_PATH}")
    print(f"💾 Vectorizer saved at: {VECTORIZER_PATH}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Train incident text classifier")
    parser.add_argument("--data", required=True, help="Path to CSV: desc,category")
    parser.add_argument("--test-size", type=float, default=0.2)
    args = parser.parse_args()
    train(args.data, test_size=args.test_size)
