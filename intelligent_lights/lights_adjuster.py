from typing import Set, List, Tuple, Dict

from intelligent_lights.cells.room import Room
from intelligent_lights.cells.sector import Sector
from intelligent_lights.light import Light


class LightsAdjuster:
    def __init__(self):
        pass

    def process(self, sensors: Set[Tuple[int, int]], lights: List[Light], sectors: List[Sector], rooms: List[Room],
                should_light: Dict[Tuple[int, int], bool]):

        for sensor, _ in filter(lambda x: not x[1], should_light.items()):
            sector = self._find_sector_for_cell(*sensor, sectors)
            if sector:
                should_off = filter(lambda p: sector.is_cell_in(p.x, p.y), lights)
                for light in should_off:
                    light.light_level = 0



    @staticmethod
    def _find_sector_for_cell(x, y, sectors: List[Sector]):
        for sector in sectors:
            if sector.is_cell_in(x, y):
                return sector

        return None
