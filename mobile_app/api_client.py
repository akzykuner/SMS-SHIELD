import requests
from typing import Optional

# Cambia esto por la IP/LAN de tu API si ejecutas en dispositivo real
API_BASE_URL = "http://127.0.0.1:8000"

def classify_text(text: str, simulate: Optional[str] = None) -> dict:
    payload = {"text": text}
    if simulate:
        payload["simulate"] = simulate
    r = requests.post(f"{API_BASE_URL}/classify", json=payload, timeout=10)
    r.raise_for_status()
    return r.json()

def send_feedback(
    text: str,
    user_label: str,
    predicted_label: Optional[str] = None,
    probability: Optional[float] = None,
    user_id: Optional[str] = None,
    notes: Optional[str] = None,
) -> dict:
    payload = {
        "text": text,
        "user_label": user_label,
        "predicted_label": predicted_label,
        "probability": probability,
        "user_id": user_id,
        "notes": notes,
    }
    r = requests.post(f"{API_BASE_URL}/feedback", json=payload, timeout=10)
    r.raise_for_status()
    return r.json()