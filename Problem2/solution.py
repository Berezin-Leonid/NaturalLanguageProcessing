from typing import List, Tuple, Set
import json

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import normalize
import numpy as np
import re

class Solution:
    def __init__(self):
        self.threshold = 0.81
        self.min_lines_in_chorus = 2

        #self.threshold = 0.9
        #self.min_lines_in_chorus = 3

        self.vectorizer = TfidfVectorizer(
            analyzer="char",
            ngram_range=(3,5),
            max_features=4_000,
            lowercase=True,
            norm=None,
        )
        

    def detect(self, tracks: List[Tuple[List[str], str]]) -> List[Set[Tuple[int, int]]]:
        return [set(self.detect_uno(lines, title)) for lines, title in tracks]
    

    def detect_uno(self, lines: List[str], title: str) -> Set[Tuple[int, int]]:
        pass
        length = len(lines)
        if length == 0:
            return []

        matrix = self.encode(lines)
        if matrix.size == 0:
            return []
        
        sim_matrix = matrix @ matrix.T
        sim_matrix = np.array(sim_matrix, dtype=float)

        all = [ ]

        for i in range(length):
            cand = [j for j in range(length) if j!= i and sim_matrix[i,j] >= self.threshold]

            if not cand:
                continue

            S = set(cand)
            S.add(i)

            while True:
                S_list = sorted(S)
                m = len(S_list)
                if m <= 1:
                    break
                removed = set()
                for p in S_list:
                    sims = sim_matrix[p, S_list]
                    cnt = int(np.sum(sims >= self.threshold) - 1)
                    if cnt < (m-1):
                        removed.add(p)
                if not removed:
                    break
                S -= removed
            
            if len(S) < 2:
                continue

            S_list = sorted(S)
            right = 0
            local_S = S_list.copy()
            while True:
                idxs = [p + right for p in local_S]
                if any(idx >= length for idx in idxs):
                    bad_idxs = [local_S[k] for k, idx in enumerate(idxs) if idx >= length]
                    new_S = [p for p in local_S if p not in bad_idxs]
                    if len(new_S) < 2:
                        break
                    local_S = new_S
                    continue

                sub = sim_matrix[
                    np.ix_([p + right for p in local_S], [p + right for p in local_S])
                ]

                m = sub.shape[0]
                if m <= 1:
                    break
                mask = ~np.eye(m ,dtype=bool)
                if not np.all(sub[mask] >= self.threshold):
                    break
                right += 1

            # --- расширяем влево ---
            left = 0
            while True:
                idxs = [p - (left + 1) for p in local_S]
                if any(idx < 0 for idx in idxs):
                    break
                sub = sim_matrix[np.ix_(idxs, idxs)]
                m = sub.shape[0]
                if m <= 1:
                    break
                mask = ~np.eye(m, dtype=bool)
                if not np.all(sub[mask] >= self.threshold):
                    break
                left += 1

            block_len = left + right
            if block_len >= int(self.min_lines_in_chorus) and len(local_S) >= 2:
                spans = []
                for p in local_S:
                    start = max(0, p - left)
                    end = min(length - 1, p + right - 1)
                    if end - start + 1 >= int(self.min_lines_in_chorus):
                        spans.append((start, end))
                spans = sorted(set(spans), key=lambda x: (x[0], x[1]))
                spans = self._remove_subspans(spans)
                if spans:
                    total_len = sum(e - s + 1 for s, e in spans)
                    all.append((spans, len(spans), total_len))

        if not all:
            return []

        # выбираем лучший вариант
        uniq = {}
        for spans, num_rep, total_len in all:
            key = tuple(spans)
            if key not in uniq:
                uniq[key] = (num_rep, total_len)
            else:
                old = uniq[key]
                if num_rep > old[0] or (num_rep == old[0] and total_len > old[1]):
                    uniq[key] = (num_rep, total_len)

        best_spans = sorted(
            uniq.items(), key=lambda x: (x[1][0], x[1][1]), reverse=True
        )[0][0]

        return list(best_spans)

        
    def encode(self, lines: list[str]) -> np.ndarray:
        norm_lines = [self._normalize_line(x) for x in lines]
        vectors = self.vectorizer.fit_transform(norm_lines)
        vectors = normalize(vectors, norm="l2", copy=False)
        vectors = vectors.toarray().astype(float)
        return vectors

    @staticmethod
    def _normalize_line(s: str) -> str:
        s = s.strip().lower()
        s = re.sub(r"\(.*?\)", "", s)
        s = re.sub(r"\s+", " ", s).strip()
        return s


    def _remove_subspans(self, spans):
        """
        Убирает интервалы, полностью содержащиеся в других.
        """
        if not spans:
            return []
        spans_sorted = sorted(spans, key=lambda x: (x[0], -x[1]))
        keep = []
        for s, e in spans_sorted:
            if not any(ks <= s and e <= ke for ks, ke in keep):
                keep.append((s, e))
        return keep

    def load_tracks(self):

        with open("tracks.json", "r", encoding="utf-8") as f:
            data = json.load(f)

        self.tracks_input = [(item["lines"], item["title"]) for item in data]
        self.true_choruses = [set(tuple(pair) for pair in item["chorus"]) for item in data]
        
        print(len(data))





if __name__ == "__main__":
    obj = Solution()