from typing import List, Tuple, Set
import json


class Solution:
    def detect(self, tracks: List[Tuple[List[str], str]]) -> List[Set[Tuple[int, int]]]:

        return [self.detect_uno(lines, title) for lines, title in tracks]
    

    def detect_uno(self, lines: List[str], title: str) -> Set[Tuple[int, int]]:
        return set()

    def load_tracks(self):

        with open("tracks.json", "r", encoding="utf-8") as f:
            data = json.load(f)

        self.tracks_input = [(item["lines"], item["title"]) for item in data]
        self.true_choruses = [set(tuple(pair) for pair in item["chorus"]) for item in data]
        
        print(len(data))





if __name__ == "__main__":
    obj = Solution()
    obj.load_tracks()
    obj.detect(obj.tracks_input)