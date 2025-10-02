import re

# Stopwords básicas (puedes expandir o cargar desde archivo en tests_data/stopwords.txt)
STOPWORDS = {"el", "la", "los", "las", "de", "y", "en", "a", "un", "una", "mismo"}

def preprocess_text(text: str):
    """
    Preprocesa un texto:
    - Convierte a minúsculas
    - Elimina caracteres no alfabéticos
    - Tokeniza por espacios
    - Elimina stopwords
    """
    if not text.strip():
        return []

    # 1. Minúsculas
    text = text.lower()

    # 2. Solo letras (reemplaza todo lo que no sea a-z con espacio)
    text = re.sub(r"[^a-záéíóúüñ]", " ", text)

    # 3. Tokenizar
    tokens = text.split()

    # 4. Eliminar stopwords
    tokens = [t for t in tokens if t not in STOPWORDS]

    return tokens
