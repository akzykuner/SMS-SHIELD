import pytest
from ml_model.src.features.url_features import has_short_url

import pytest

@pytest.mark.parametrize("text,expected", [
    ("URGENTE: verifique su cuenta en bit.ly/xyz123", 1),
    ("Revisa aquí: https://tinyurl.com/abcd)", 1),  # paréntesis de cierre
    ("Síguenos en t.co/xyz", 1),
    ("Nos vemos a las 7pm", 0),
    ("Visita banco-nacion.pe para más info", 0),

])
def test_has_short_url_variantes(text, expected):
    assert has_short_url(text) == expected
