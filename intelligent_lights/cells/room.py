from typing import List


class Room:
    def __init__(self, rects: List[List[int]], label: str):
        self.rects = rects
        self.label = label

    def is_cell_in(self, x: int, y: int) -> bool:
        return any(self._is_cell_in_rect(x, y, r) for r in self.rects)

    @staticmethod
    def _is_cell_in_rect(x: int, y: int, rect: List[int]) -> bool:
        return rect[0] + rect[2] > x >= rect[0] and rect[1] + rect[3] > y >= rect[1]
