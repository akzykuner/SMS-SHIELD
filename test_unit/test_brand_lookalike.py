import csv
import os
import pytest
from ml_model.brand_lookalike import looks_like_brand

# Ruta al archivo CSV
DATA_FILE = os.path.join(os.path.dirname(__file__), "..", "tests_data", "brand_lookalike_cases.csv")

def load_cases():
    """Carga los casos desde el CSV."""
    with open(DATA_FILE, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            yield row["candidate"], row["brand"], int(row["expected"])

@pytest.mark.parametrize("candidate,brand,expected", load_cases())
def test_brand_lookalike_cases(candidate, brand, expected):
    assert looks_like_brand(candidate, brand) == expected
