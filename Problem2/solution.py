from typing import List, Tuple, Set
import json
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np


class Solution:
    def detect(self, tracks: List[Tuple[List[str], str]]) -> List[Set[Tuple[int, int]]]:

        return [self.detect_uno(lines, title) for lines, title in tracks]
    

    def detect_uno(self, lines: List[str], title: str) -> Set[Tuple[int, int]]:
        return set(self.merge_blocks(
                            self.find_choruses(lines=lines, track_name=title)))

    def load_tracks(self):

        with open("tracks.json", "r", encoding="utf-8") as f:
            data = json.load(f)

        self.tracks_input = [(item["lines"], item["title"]) for item in data]
        self.true_choruses = [set(tuple(pair) for pair in item["chorus"]) for item in data]
        


  

    def find_choruses(self, lines, track_name=None, sim_threshold=0.99, min_len=2):
        vectorizer = TfidfVectorizer().fit(lines)
        X = vectorizer.transform(lines)
        sim_matrix = cosine_similarity(X)
        n = len(lines)
        candidates = []

        for i in range(n):
            for j in range(i + min_len, n):
                for L in range(min_len, n - max(i, j) + 1):
                    block1 = list(range(i, i + L))
                    block2 = list(range(j, j + L))
                    sims = [sim_matrix[a, b] for a, b in zip(block1, block2)]
                    if np.mean(sims) >= sim_threshold:
                        candidates.append((i, i + L - 1))
                        candidates.append((j, j + L - 1))
                    else:
                        break

        # --- убираем дубли ---
        def overlap(a, b):
            return not (a[1] < b[0] or b[1] < a[0])

        unique = []
        for c in candidates:
            if not any(overlap(c, u) for u in unique):
                unique.append(c)

        return unique
    
    
    def merge_blocks(self, blocks, max_gap=1):
        if not blocks:
            return []

        blocks = sorted(blocks)
        merged = [blocks[0]]
        for start, end in blocks[1:]:
            prev_start, prev_end = merged[-1]
            if start <= prev_end + max_gap:
                merged[-1] = (prev_start, max(end, prev_end))
            else:
                merged.append((start, end))
        return merged




if __name__ == "__main__":
    obj = Solution()
    obj.load_tracks()
    print(obj.tracks_input[0])

    print(obj.detect(obj.tracks_input[0:1:1]))

    #choruses = obj.detect([(lines, "Track")])
    #print(choruses)
