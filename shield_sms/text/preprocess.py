
import re

SPANISH_STOPWORDS = {
    "de","la","que","el","en","y","a","los","del","se","las","por","un","para","con","no",
    "una","su","al","lo","como","más","pero","sus","le","ya","o","este","sí","porque","esta",
    "entre","cuando","muy","sin","sobre","también"
}

def preprocess_text(text: str):
    if not text:
        return []
    t = text.lower()
    # remove punctuation and special chars, keep urls chars
    t = re.sub(r"[^\w/@:\.\- ]+", " ", t, flags=re.UNICODE)
    # collapse spaces
    t = re.sub(r"\s+", " ", t).strip()
    tokens = t.split(" ")
    tokens = [tok for tok in tokens if tok and tok not in SPANISH_STOPWORDS]
    return tokens
