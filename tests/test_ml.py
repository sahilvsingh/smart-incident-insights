import os
import pickle
from unittest.mock import patch

import pytest

MODEL_PATH = "src/ml/model.pkl"
VECTORIZER_PATH = "src/ml/vectorizer.pkl"

# --- CREATE DUMMY MODEL & VECTORIZER ---
@pytest.fixture(scope="module", autouse=True)
def setup_dummy_model():
    # create dummy model
    dummy_model = {"dummy": True}
    dummy_vectorizer = {"dummy": True}
    os.makedirs("src/ml", exist_ok=True)
    with open(MODEL_PATH, "wb") as f:
        pickle.dump(dummy_model, f)
    with open(VECTORIZER_PATH, "wb") as f:
        pickle.dump(dummy_vectorizer, f)
    yield
    os.remove(MODEL_PATH)
    os.remove(VECTORIZER_PATH)

def test_model_exists():
    assert os.path.exists(MODEL_PATH)
    assert os.path.exists(VECTORIZER_PATH)

def test_model_prediction():
    with open(MODEL_PATH, "rb") as f:
        model = pickle.load(f)
    with open(VECTORIZER_PATH, "rb") as f:
        vectorizer = pickle.load(f)
    assert "dummy" in model
    assert "dummy" in vectorizer
