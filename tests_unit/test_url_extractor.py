import pytest
from ml_model.src.features.url_features import extract_urls

def _find_first(text):
    urls = extract_urls(text)
    assert urls, "No se extrajo ninguna URL"
    return urls[0]

def test_extrae_ip_host_type_ip():
    u = _find_first("Visite http://192.168.1.1 para activar su cuenta")
    assert u["domain"] == "192.168.1.1"
    assert u["host_type"] == "ip"

def test_extrae_dominio_host_type_domain():
    u = _find_first("https://banco-nacion.pe/login")
    assert u["domain"] == "banco-nacion.pe"
    assert u["host_type"] == "domain"

def test_sin_url_no_falla():
    urls = extract_urls("Nos vemos 7pm")
    assert urls == []

def test_url_sin_esquema():
    u = _find_first("Acceda a banco-nacion.pe/clave, gracias.")
    assert u["domain"] == "banco-nacion.pe"
    assert u["host_type"] == "domain"

