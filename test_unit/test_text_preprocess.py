import csv
import os
import pytest
from ml_model.text_preprocess import preprocess_text

# Ruta al CSV de casos de prueba
DATA_FILE = os.path.join(os.path.dirname(__file__), "..", "tests_data", "text_preprocess_cases.csv")

def load_cases():
    cases = []
    with open(DATA_FILE, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            input_text = row["input_text"]
            # Convertir la lista esperada de tokens desde string → lista real
            expected_tokens = eval(row["expected_tokens"])
            cases.append((input_text, expected_tokens))
    return cases

@pytest.mark.parametrize("input_text,expected_tokens", load_cases())
def test_preprocess_cases(input_text, expected_tokens):
    result = preprocess_text(input_text)
    assert result == expected_tokens
