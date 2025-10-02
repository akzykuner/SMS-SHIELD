import time
import csv
import numpy as np
from fastapi.testclient import TestClient
from api.app import app

client = TestClient(app)

def test_e2e_throughput__smoke_batch_requests():
    texts = ["URGENTE: verifique su cuenta en bit.ly/xyz123" if i % 2 == 0 else "Nos vemos a las 7pm" for i in range(50)]
    latencies = []

    for t in texts:
        start = time.time()
        response = client.post("/classify", json={"text": t})
        elapsed = time.time() - start
        latencies.append(elapsed)
        assert response.status_code == 200

    p95_latency = float(np.percentile(latencies, 95))

    with open("e2e_throughput_report.csv", "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Batch Size", "p95 Latency"])
        writer.writerow([len(texts), p95_latency])

    print(f"[E2E] Batch size: {len(texts)}, p95 latency: {p95_latency:.4f}s")
