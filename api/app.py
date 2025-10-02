from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

class ClassifyRequest(BaseModel):
    text: str
    simulate: Optional[str] = None

def classify_text(text: str):
    # Implementar la lógica de clasificación
    label = "smishing" if "URGENTE" in text else "ham"
    verification_status = "ok"
    return {"label": label, "verification_status": verification_status}

def simulate_timeout(simulate_value: Optional[str]):
    if simulate_value == "timeout":
        return {"verification_status": "pending"}
    return None

@app.post("/classify")
def classify(request: ClassifyRequest):
    timeout_response = simulate_timeout(request.simulate)
    if timeout_response:
        return timeout_response
    try:
        result = classify_text(request.text)
        return result
    except Exception:
        raise HTTPException(status_code=500, detail="Error processing the request")
