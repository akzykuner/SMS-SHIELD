from dataclasses import dataclass, field
from typing import List, Optional
import json
import os
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer

from .url_utils import extract_urls, is_short_url, normalize_url, looks_like_brand
from ..text.preprocess import preprocess_text


@dataclass
class FeatureSchema:
    tfidf_order: List[str] = field(default_factory=list)
    struct_order: List[str] = field(default_factory=list)

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            tfidf_order=data.get("tfidf_features", []),
            struct_order=data.get("structural_features", [])
        )


class CustomVectorizer:
    def __init__(self, schema_path: Optional[str] = None):
        if schema_path and os.path.exists(schema_path):
            with open(schema_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            self.schema = FeatureSchema.from_dict(data)
        else:
            default_vocab = ["gana", "bono", "ahora", "urgente", "cuenta", "verifique"]
            self.schema = FeatureSchema(
                tfidf_order=default_vocab,
                struct_order=["caps_ratio", "exclam_count", "token_len_avg", "has_short_url", "looks_like_brand"]
            )
        self.vectorizer = TfidfVectorizer(
            ngram_range=(1, 2),
            vocabulary=self.schema.tfidf_order,
            tokenizer=preprocess_text,
            preprocessor=lambda x: x,
        )

    def _struct_features(self, text: str) -> np.ndarray:
        letters = sum(c.isalpha() for c in text)
        caps_ratio = (sum(c.isupper() for c in text) / letters) if letters else 0.0
        exclam_count = text.count("!")
        tokens = preprocess_text(text)
        token_len_avg = (sum(len(t) for t in tokens) / len(tokens)) if tokens else 0.0

        urls = extract_urls(text)
        has_short = 1 if any(is_short_url(u) for u in urls) else 0
        like_brand = 0
        for u in urls:
            info = normalize_url(u)
            if looks_like_brand(info["domain"], "banco-nacion.pe"):
                like_brand = 1
                break
        return np.array([caps_ratio, exclam_count, token_len_avg, has_short, like_brand], dtype=float)

    def fit(self, texts: List[str]):
        self.vectorizer.fit(texts)
        return self

    def transform(self, texts: List[str]) -> np.ndarray:
        tfidf = self.vectorizer.transform(texts).toarray()
        struct = np.vstack([self._struct_features(t) for t in texts])
        return np.hstack([tfidf, struct])

    def fit_transform(self, texts: List[str]) -> np.ndarray:
        self.fit(texts)
        return self.transform(texts)

    def feature_dimension(self) -> int:
        return len(self.schema.tfidf_order) + len(self.schema.struct_order)
