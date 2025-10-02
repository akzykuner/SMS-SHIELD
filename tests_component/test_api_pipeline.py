from fastapi.testclient import TestClient
from api.app import app

client = TestClient(app)

def test_api_pipeline__classify_short_url():
    payload = {"text": "URGENTE: verifique su cuenta en bit.ly/xyz123"}
    r = client.post("/classify", json=payload)
    assert r.status_code == 200
    data = r.json()
    assert data["label"] in ("smishing", "ham")
    assert data["verification_status"] == "ok"

def test_api_pipeline__timeout_simulation():
    payload = {"text": "URGENTE: verifique su cuenta en bit.ly/xyz123", "simulate": "timeout"}
    r = client.post("/classify", json=payload)
    assert r.status_code == 200
    data = r.json()
    assert data["verification_status"] == "pending"
