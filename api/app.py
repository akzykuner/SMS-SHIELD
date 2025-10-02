
from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional, Dict, Any

from shield_sms.features.vectorizer import CustomVectorizer
from shield_sms.model.classifier import Classifier

app = FastAPI(title="Shield-SMS API")

# Simple in-memory pipeline trained on a tiny golden set during startup (for demo)
VEC = CustomVectorizer(schema_path="tests_data/feature_schema.json")
CLF = Classifier(VEC)

# If golden set is available, train; else train on minimal synthetic data
try:
    import csv
    texts, labels = [], []
    with open("tests_data/golden_set.csv", "r", encoding="utf-8") as f:
        r = csv.DictReader(f)
        for row in r:
            texts.append(row["text"])
            labels.append(1 if row["label"].strip().lower()=="smishing" else 0)
    if texts:
        CLF.fit(texts, labels)
    else:
        raise RuntimeError("Empty golden set")
except Exception:
    CLF.fit(
        ["Nos vemos a las 7pm", "URGENTE: verifique su cuenta en bit.ly/xyz123"],
        [0, 1]
    )

class ClassifyIn(BaseModel):
    text: str
    simulate: Optional[str] = None  # "timeout" to emulate external dependency issues

class ClassifyOut(BaseModel):
    label: str
    proba: float
    verification_status: str

@app.post("/classify", response_model=ClassifyOut)
def classify(inp: ClassifyIn):
    proba = float(CLF.predict_proba([inp.text])[0][1])
    label = "smishing" if proba >= 0.5 else "ham"

    # simulate external verifier status
    if inp.simulate == "timeout":
        status = "pending"
    else:
        status = "ok"

    return ClassifyOut(label=label, proba=proba, verification_status=status)
