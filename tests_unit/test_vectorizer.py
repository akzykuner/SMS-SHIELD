import pytest
from vectorizer import Vectorizer

@pytest.fixture
def vectorizador():
    return Vectorizer()

def test_mismo_tamano_y_estructura(vectorizador):
    texto1 = "Texto de prueba uno!"
    texto2 = "Otro texto para prueba."
    
    vec1 = vectorizador.vectorize(texto1)
    vec2 = vectorizador.vectorize(texto2)
    
    # Ambos vectores deben tener la misma longitud
    assert len(vec1) == len(vec2)
    
    # Verificamos tipos de las últimas posiciones (rasgos estructurales)
    caps_ratio = vec1[-3]
    exclam_count = vec1[-2]
    token_len = vec1[-1]

    assert isinstance(caps_ratio, float)
    assert isinstance(exclam_count, int)
    assert isinstance(token_len, int)
