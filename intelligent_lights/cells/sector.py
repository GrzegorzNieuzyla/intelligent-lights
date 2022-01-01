from typing import List


class Sector:
    def __init__(self, bounds: List[int]):
        self.bounds = bounds

    def is_cell_in(self, x: int, y: int) -> bool:
        return self.bounds[0] + self.bounds[2] > x >= self.bounds[0] and self.bounds[1] + self.bounds[3] > y > \
               self.bounds[3]
