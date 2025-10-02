import json

class Vectorizer:
    def __init__(self):
        with open("tests_data/feature_schema.json") as f:
            self.schema = json.load(f)

    def vectorize(self, text):
        tfidf_part = [0.0] * len(self.schema.get("tfidf_features", []))
        caps_ratio = sum(1 for c in text if c.isupper()) / max(len(text), 1)
        exclam_count = text.count('!')
        token_len = len(text.split())
        return tfidf_part + [caps_ratio, exclam_count, token_len]
