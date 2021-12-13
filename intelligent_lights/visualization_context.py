from dataclasses import dataclass
from typing import List, Tuple

from intelligent_lights.cells.cell import Cell


@dataclass
class VisualizationContext:
    grid: List[List[Cell]]
    person_positions: List[Tuple[int, int]]
    time: str
