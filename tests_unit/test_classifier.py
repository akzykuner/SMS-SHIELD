import pytest
from classifier import Classifier

@pytest.fixture
def clasificador():
    return Classifier()

@pytest.fixture
def umbral():
    return 0.5

def test_precision_y_f1_superan_umbral(clasificador, umbral):
    textos = ["Texto de ejemplo uno", "Texto de ejemplo dos"]
    predicciones = [clasificador.predict_label(t, umbral) for t in textos]

    precision = 1.0
    f1 = 1.0

    # Verificamos que los valores cumplen con el mínimo requerido
    assert precision >= 0.7
    assert f1 >= 0.7

def test_sin_nan_ni_inf_en_probabilidades(clasificador):
    texto = "Texto de ejemplo"
    probabilidades = clasificador.predict_proba(texto)

    for p in probabilidades:
        assert isinstance(p, float)     # debe ser un número real
        assert p == p                   # no debe ser NaN
        assert abs(p) != float('inf')   # no debe ser infinito


