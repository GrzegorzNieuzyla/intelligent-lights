from typing import Set, List, Tuple, Dict

from intelligent_lights.cells.room import Room
from intelligent_lights.cells.sector import Sector
from intelligent_lights.light import Light


class LightsAdjuster:
    def __init__(self):
        pass

    def process(self, sensors: Set[Tuple[int, int, int]], lights: List[Light], sectors: List[Sector], rooms: List[Room],
                should_light: Dict[Tuple[int, int], bool]):

        self.turn_off_unnecessary_lights(lights, sectors, should_light)

        for detection_point, _ in filter(lambda x: x[1], should_light.items()):
            room = self._find_room_for_cell(*detection_point, rooms)
            sensors_in_room = filter(lambda p: room.is_cell_in(p.x, p.y), sensors)
            light_in_room = filter(lambda p: room.is_cell_in(p.x, p.y), lights)
            sensors_to_adjust = []
            for x, y in sensors_in_room:
                xd, yd = detection_point
                if abs(xd-x) + abs(yd-y) <= 2:
                    sensors_to_adjust.append((x, y))
                    break
            else:
                sensors_to_adjust = sensors_in_room

            # for l in light_in_room:



    def turn_off_unnecessary_lights(self, lights, sectors, should_light):
        for detection_point, _ in filter(lambda x: not x[1], should_light.items()):
            sector = self._find_sector_for_cell(*detection_point, sectors)
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

    @staticmethod
    def _find_room_for_cell(x, y, rooms: List[Room]):
        for room in rooms:
            if room.is_cell_in(x, y):
                return room

        return None


    def _cal(x, y, rooms: List[Room]):
        for room in rooms:
            if room.is_cell_in(x, y):
                return room

        return None