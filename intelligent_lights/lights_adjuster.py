from typing import Set, List, Tuple, Dict

from intelligent_lights.cells.room import Room
from intelligent_lights.cells.sector import Sector
from intelligent_lights.light import Light


class LightsAdjuster:
    EPSILON = 5
    REQUIRED_LIGHT = 100

    def __init__(self):
        self.to_adjust = {}

    def process(self, sensors: Set[Tuple[int, int, int]], lights: List[Light], sectors: List[Sector], rooms: List[Room],
                should_light: Dict[Tuple[int, int], bool]):

        self.turn_off_unnecessary_lights(lights, sectors, should_light)

        for detection_point, _ in filter(lambda x_: x_[1], should_light.items()):
            # room = self.find_room_for_cell(*detection_point, rooms)
            sector = self.find_sector_for_cell(*detection_point, sectors)
            if not sector: continue
            sensors_in_sector = list(filter(lambda p: sector.is_cell_in(p[0], p[1]), sensors))
            light_in_sector = list(filter(lambda p: sector.is_cell_in(p.x, p.y), lights))
            for x, y, val in sensors_in_sector:
                xd, yd = detection_point
                if abs(xd-x) + abs(yd-y) <= 2:
                    sensors_to_adjust = [(x, y, val)]
                    break
            else:
                sensors_to_adjust = sensors_in_sector
            value = self._calculate_light_value(*detection_point, sensors_to_adjust)
            if value < self.REQUIRED_LIGHT:
                if detection_point in self.to_adjust:
                    ratio = (value - self.to_adjust[detection_point]) / self.EPSILON
                    if ratio == 0:
                        del self.to_adjust[detection_point]
                        return
                    req = (self.REQUIRED_LIGHT + self.EPSILON - value) / ratio
                    for light in light_in_sector:
                        light.light_level += req
                    del self.to_adjust[detection_point]
                else:
                    for light in light_in_sector:
                        light.light_level += self.EPSILON
                    self.to_adjust[detection_point] = value
            elif detection_point in self.to_adjust:
                del self.to_adjust[detection_point]

    def turn_off_unnecessary_lights(self, lights, sectors, should_light):
        for detection_point, _ in filter(lambda x: not x[1], should_light.items()):
            if detection_point in self.to_adjust:
                del self.to_adjust[detection_point]
            sector = self.find_sector_for_cell(*detection_point, sectors)
            if sector:
                should_off = filter(lambda p: sector.is_cell_in(p.x, p.y), lights)
                for light in should_off:
                    light.light_level = 0

    @staticmethod
    def find_sector_for_cell(x, y, sectors: List[Sector]):
        for sector in sectors:
            if sector.is_cell_in(x, y):
                return sector

        return None

    @staticmethod
    def find_room_for_cell(x, y, rooms: List[Room]):
        for room in rooms:
            if room.is_cell_in(x, y):
                return room

        return None

    @staticmethod
    def _calculate_light_value(x, y, sensors):
        if len(sensors) == 1:
            return sensors[0][2]
        dists = []
        for sensor in sensors:
            dx = x - sensor[0]
            dy = y - sensor[1]
            dists.append([dx*dx + dy*dy, sensor[2]])
        total = sum(i[0] for i in dists)
        for dist in dists:
            dist[0] = 1 - dist[0] / total
        value = sum(x[0] * x[1] for x in dists)
        return value
