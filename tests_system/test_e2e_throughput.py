
import time
import numpy as np
from fastapi.testclient import TestClient
from api.app import app

def test_e2e_throughput__smoke_batch_requests():
    client = TestClient(app)
    texts = [
        "URGENTE: verifique su cuenta en bit.ly/xyz123" if i % 2 == 0 else "Nos vemos a las 7pm"
        for i in range(20)
    ]
    latencies = []
    for t in texts:
        t0 = time.time()
        r = client.post("/classify", json={"text": t})
        t1 = time.time()
        assert r.status_code == 200
        latencies.append(t1 - t0)
    # compute p95 for reporting (no strict assertion to avoid env flakiness)
    p95 = float(np.percentile(latencies, 95))
    # Ensure latencies are finite and non-negative
    assert all(np.isfinite(lat) and lat >= 0 for lat in latencies)
    # Attach as test artifact via printed log (visible in CI)
    print(f"[E2E] batch={len(texts)} p95={p95:.4f}s")
