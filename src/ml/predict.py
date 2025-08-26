from typing import Optional
from src.ml.model import load_model_and_vectorizer

_model = None
_vectorizer = None

def _load_once():
    global _model, _vectorizer
    if _model is None or _vectorizer is None:
        _model, _vectorizer = load_model_and_vectorizer()

def predict_category(description: str) -> Optional[str]:
    try:
        _load_once()
        X = _vectorizer.transform([description])
        pred = _model.predict(X)[0]
        return str(pred)
    except Exception as exc:
        print(f"❌ Prediction failed: {exc}")
        return "unknown"
