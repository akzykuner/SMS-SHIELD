import time
import numpy as np
from fastapi.testclient import TestClient
from api.app import app

client = TestClient(app)

def test_e2e_throughput__smoke_batch_requests():
    texts = ["URGENTE: verifique su cuenta en bit.ly/xyz123" for _ in range(50)]
    latencies = []
    start_time = time.time()

    for text in texts:
        t0 = time.time()
        response = client.post("/classify", json={"text": text})
        t1 = time.time()
        latencies.append(t1 - t0)
        assert response.status_code == 200

    elapsed = time.time() - start_time
    p95 = float(np.percentile(latencies, 95))

    # Condición esperada para luz roja: toma más de 10 segundos o p95 muy alto
    assert elapsed > 10 or p95 > 2.0  # Estos valores son arbitrarios para hacer fallar

    print(f"Batch time: {elapsed}s, p95 latency: {p95}s")
