from dataclasses import dataclass
from typing import List, Tuple, Set, Dict

from intelligent_lights.cells.cell import Cell
from intelligent_lights.cells.exit import Exit
from intelligent_lights.cells.room import Room
from intelligent_lights.cells.window import Window
from intelligent_lights.light import Light


@dataclass
class VisualizationContext:
    grid: List[List[Cell]]
    person_visible_positions: Set[Tuple[int, int]]
    person_not_visible_positions: Set[Tuple[int, int]]
    light_positions: Dict[Tuple[int, int], Light]
    sensor_positions: Set[Tuple[int, int]]
    camera_positions: Set[Tuple[int, int]]
    exits: List[Exit]
    rooms: List[Room]
    windows: List[Window]
    cell_size_in_meter: float
    time: str
    sun_power: int
    sun_position: List[int]
    sun_distance: int
    detection_points: Set[Tuple[int, int]]
