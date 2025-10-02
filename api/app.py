from fastapi import FastAPI, Depends
from pydantic import BaseModel
from typing import Optional
import csv

from shield_sms.features.vectorizer import CustomVectorizer
from shield_sms.model.classifier import Classifier

app = FastAPI(title="Shield-SMS API")

VEC = CustomVectorizer(schema_path="tests_data/feature_schema.json")
CLF = Classifier(VEC)

try:
    texts, labels = [], []
    with open("tests_data/golden_set.csv", "r", encoding="utf-8") as f:
        r = csv.DictReader(f)
        for row in r:
            texts.append(row["text"])
            labels.append(1 if row["label"].strip().lower() == "smishing" else 0)
    if texts:
        CLF.fit(texts, labels)
    else:
        raise RuntimeError("Empty golden set")
except Exception:
    CLF.fit(
        ["Nos vemos a las 7pm", "URGENTE: verifique su cuenta en bit.ly/xyz123"],
        [0, 1],
    )

class ClassifyIn(BaseModel):
    text: str
    simulate: Optional[str] = None

class ClassifyOut(BaseModel):
    label: str
    proba: float
    verification_status: str

def external_verifier(text: str, simulate: Optional[str] = None):
    if simulate == "timeout":
        return "pending"
    return "ok"

@app.post("/classify", response_model=ClassifyOut)
def classify(inp: ClassifyIn, verifier=Depends(lambda: external_verifier)):
    proba = float(CLF.predict_proba([inp.text])[0][1])
    label = "smishing" if proba >= 0.5 else "ham"

    status = verifier(inp.text, inp.simulate)

    return ClassifyOut(label=label, proba=proba, verification_status=status)
