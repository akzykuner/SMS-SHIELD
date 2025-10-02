
import hashlib
import numpy as np
from dataclasses import dataclass
from typing import List, Tuple
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, f1_score, recall_score

@dataclass
class Metrics:
    accuracy: float
    recall: float
    f1: float

class Classifier:
    def __init__(self, vectorizer):
        self.vectorizer = vectorizer
        self.model = LogisticRegression(max_iter=200)

    def fit(self, texts: List[str], labels: List[int]):
        X = self.vectorizer.fit_transform(texts)
        y = np.array(labels, dtype=int)
        self.model.fit(X, y)
        # create a simple checksum of the learned coefficients for reproducibility checks
        coefs = np.nan_to_num(self.model.coef_, nan=0.0).tobytes()
        self.checksum = hashlib.sha256(coefs).hexdigest()
        return self

    def predict_proba(self, texts: List[str]) -> np.ndarray:
        X = self.vectorizer.transform(texts)
        return self.model.predict_proba(X)  # [:,1] is probability of class 1

    def predict_label(self, texts: List[str], threshold: float = 0.5) -> List[int]:
        proba = self.predict_proba(texts)[:, 1]
        return (proba >= threshold).astype(int).tolist()

    @staticmethod
    def compute_metrics(y_true: List[int], y_pred: List[int]) -> Metrics:
        return Metrics(
            accuracy=accuracy_score(y_true, y_pred),
            recall=recall_score(y_true, y_pred, zero_division=0),
            f1=f1_score(y_true, y_pred, zero_division=0)
        )
