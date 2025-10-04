from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional

from api.schemas import ClassifyRequest, FeedbackRequest
from api.deps import get_model, score_text, THRESHOLD
from api.feedback import record_feedback

try:
    # Reutilizo tu extractor robusto de URLs
    from ml_model.src.features.url_features import extract_urls as extract_urls_ml
except Exception:
    extract_urls_ml = None

app = FastAPI(title="Shield-SMS API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # en producción, restringe esto
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def _startup():
    # Entrena/carga el modelo ligero al iniciar
    get_model()

def simulate_timeout(simulate_value: Optional[str]):
    if simulate_value == "timeout":
        return {"verification_status": "pending"}
    return None

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/classify")
def classify(request: ClassifyRequest):
    timeout = simulate_timeout(request.simulate)
    if timeout:
        return timeout

    text = request.text or ""
    try:
        # URLs detectadas
        urls_info = []
        if extract_urls_ml:
            urls_info = extract_urls_ml(text)

        # Score del modelo
        label, proba = score_text(text)

        return {
            "label": label,
            "probability": proba,
            "verification_status": "ok",
            "urls": urls_info,
            "meta": {"threshold": THRESHOLD},
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing the request: {e}")

@app.post("/feedback")
def feedback(payload: FeedbackRequest):
    try:
        record_feedback(
            text=payload.text,
            user_label=payload.user_label,
            predicted_label=payload.predicted_label,
            probability=payload.probability,
            user_id=payload.user_id,
            notes=payload.notes,
        )
        return {"status": "ok"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error saving feedback: {e}")
    
@app.get("/")
def root():
    return {"status": "Achalma bot"}