import csv
from pathlib import Path
from typing import List, Tuple
from shield_sms.features.vectorizer import CustomVectorizer
from shield_sms.model.classifier import Classifier as SMSClassifier

DATA_CSV = Path("tests_data/golden_set.csv")
THRESHOLD = 0.5

_MODEL = None
_VECTORIZER = None

LABEL_TO_INT = {"ham": 0, "smishing": 1}
INT_TO_LABEL = {v: k for k, v in LABEL_TO_INT.items()}

def load_training_data(csv_path: Path) -> Tuple[List[str], List[int]]:
    texts: List[str] = []
    labels: List[int] = []
    if not csv_path.exists():
        # fallback mínimo si no está el CSV
        texts = [
            "URGENTE: verifique su cuenta en bit.ly/xyz123",
            "Nos vemos a las 7pm",
        ]
        labels = [1, 0]
        return texts, labels

    with csv_path.open("r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            t = (row.get("text") or "").strip()
            lbl = (row.get("label") or "ham").strip().lower()
            if t:
                texts.append(t)
                labels.append(LABEL_TO_INT.get(lbl, 0))
    return texts, labels

def get_model() -> Tuple[CustomVectorizer, SMSClassifier]:
    global _MODEL, _VECTORIZER
    if _MODEL is None or _VECTORIZER is None:
        _VECTORIZER = CustomVectorizer()
        _MODEL = SMSClassifier(_VECTORIZER)
        texts, labels = load_training_data(DATA_CSV)
        _MODEL.fit(texts, labels)
    return _VECTORIZER, _MODEL

def score_text(text: str) -> Tuple[str, float]:
    _, model = get_model()
    proba = float(model.predict_proba([text])[0][1])
    label_int = 1 if proba >= THRESHOLD else 0
    return INT_TO_LABEL[label_int], proba