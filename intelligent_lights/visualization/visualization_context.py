from dataclasses import dataclass
from typing import List, Tuple, Set, Dict

from intelligent_lights.cells.cell import Cell
from intelligent_lights.light import Light


@dataclass
class VisualizationContext:
    grid: List[List[Cell]]
    person_positions: Set[Tuple[int, int]]
    light_positions: Dict[Tuple[int, int], Light]
    time: str
