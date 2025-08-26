import os
import joblib

THIS_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(THIS_DIR, "incident_model.pkl")
VECTORIZER_PATH = os.path.join(THIS_DIR, "vectorizer.pkl")

def ensure_artifacts_exist():
    if not (os.path.exists(MODEL_PATH) and os.path.exists(VECTORIZER_PATH)):
        raise FileNotFoundError(
            "Model artifacts not found. Train first with:\n"
            "python -m src.ml.train --data src/ml/dataset/incidents.csv"
        )

def load_model_and_vectorizer():
    ensure_artifacts_exist()
    model = joblib.load(MODEL_PATH)
    vectorizer = joblib.load(VECTORIZER_PATH)
    return model, vectorizer
