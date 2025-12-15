# solution.py
"""
Класс Solution — интерфейс для тестирующей системы.
Загружает обученную CRF-модель и выполняет инференс.
"""

import os
import joblib
from typing import List, Set, Tuple

from utils import tokenize_with_spans, token_features, bio_to_spans

MODEL_PATH = "model.joblib"


class Solution:
    def __init__(self, model_path: str = MODEL_PATH):
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"Модель не найдена: {model_path}")
        self.model = joblib.load(model_path)

    def predict(self, texts: List[str]) -> List[Set[Tuple[int, int, str]]]:
        """
        Принимает список текстов и возвращает список множеств сущностей.
        Каждое множество содержит (start_char, end_char, label).
        """
        results = []
        for text in texts:
            tokens = tokenize_with_spans(text)
            feats = [token_features(tokens, i) for i in range(len(tokens))]
            tags = self.model.predict_single(feats)
            spans = bio_to_spans(tokens, tags)
            results.append(set(spans))
        return results
