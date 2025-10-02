import difflib

# Tabla básica de sustituciones confusas
SUBSTITUTIONS = {
    "0": "o",
    "1": "l",
    "rn": "m",
    "-": ""   # tolerar guiones extra
}

def normalize_domain(domain: str) -> str:
    """Aplica sustituciones heurísticas a un dominio."""
    normalized = domain.lower()
    for fake, real in SUBSTITUTIONS.items():
        normalized = normalized.replace(fake, real)
    return normalized

def looks_like_brand(candidate: str, brand: str, threshold: float = 0.85) -> int:
    """
    Devuelve 1 si candidate se parece al dominio de brand,
    0 en caso contrario.
    Usa similitud difusa con umbral configurable.
    """
    norm_candidate = normalize_domain(candidate)
    norm_brand = normalize_domain(brand)

    if candidate == brand:
        return 0  # dominio exacto, no es lookalike

    # Similaridad de secuencias
    similarity = difflib.SequenceMatcher(None, norm_candidate, norm_brand).ratio()

    return 1 if similarity >= threshold else 0
