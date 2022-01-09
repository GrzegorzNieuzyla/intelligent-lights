from typing import Set, List, Tuple

from bresenham import bresenham

from intelligent_lights.cells.cell_type import CellType
from intelligent_lights.cells.room import Room
from intelligent_lights.sensors import Sensor


class BlindsAdjuster:
    MAX_REQUIRED_LIGHT = 200
    MAX_SENSOR_DISTANCE = 5

    def __init__(self, detection_points: List[Tuple[int, int]], rooms: List[Room], sensors: Set[Sensor],
                 windows: List[Tuple[int, int]], grid, cell_size: float):
        self.detection_points = detection_points
        self.rooms = rooms
        self.sensors = sensors
        self.windows = windows
        self.grid = grid
        self.cell_size = cell_size
        self.applicable_sensors = {}
        self.windows_positions = []
        self.sensor_distance = self.MAX_SENSOR_DISTANCE / self.cell_size
        self.preprocess()
        self.level = 1
        self.min_level = 1
        self.max_level = 1e-3

    def preprocess(self):
        for detection_point in self.detection_points:
            self.applicable_sensors[detection_point] = self.find_applicable_sensors(detection_point)
        for w in self.windows:
            b = w.bounds
            if b[0] == 0:
                for i in range(b[3]):
                    self.windows_positions.append((0, b[1] + i))
            if b[1] == 0:
                for i in range(b[2]):
                    self.windows_positions.append((b[0] + i, 0))

    def process(self):
        for detection_point in self.detection_points:
            sensors_to_adjust = self.find_applicable_sensors(detection_point)
            value = self._calculate_light_value(*detection_point, sensors=sensors_to_adjust)

            # adjust blinds
            if value > self.MAX_REQUIRED_LIGHT and self._is_window_in_straight_line(*detection_point):
                self.level = max(self.MAX_REQUIRED_LIGHT / value, self.max_level)
            if value <= self.MAX_REQUIRED_LIGHT and self._is_window_in_straight_line(*detection_point):
                value = value if value != 0 else 1e-6
                self.level = min(self.MAX_REQUIRED_LIGHT / value, self.min_level)

    def find_applicable_sensors(self, detection_point: Tuple[int, int]) -> List[Sensor]:
        if detection_point in self.applicable_sensors:
            return self.applicable_sensors[detection_point]
        room = self.find_room_for_cell(*detection_point)
        sensors_in_room = list(filter(lambda p: room.is_cell_in(p.x, p.y), self.sensors))
        for sensor in sensors_in_room:
            xd, yd = detection_point
            if abs(xd - sensor.x) + abs(yd - sensor.y) <= 3:
                sensors_to_adjust = [sensor]
                break
        else:
            sensors_to_adjust = list(
                filter(lambda s: self.dist(s.x, s.y, *detection_point) <= self.sensor_distance,
                       sensors_in_room))

        self.applicable_sensors[detection_point] = sensors_to_adjust
        return sensors_to_adjust

    def find_room_for_cell(self, x, y):
        for room in self.rooms:
            if room.is_cell_in(x, y):
                return room
        return None

    @staticmethod
    def _calculate_light_value(x: int, y: int, sensors: List[Sensor]):
        if len(sensors) == 1:
            return sensors[0].value
        dists = []
        for sensor in sensors:
            dx = x - sensor.x
            dy = y - sensor.y
            dists.append([dx * dx + dy * dy, sensor.value])
        total = sum(i[0] for i in dists)
        for dist in dists:
            dist[0] = 1 - dist[0] / total
        value = sum(x[0] * x[1] for x in dists)
        return value

    def _is_window_in_straight_line(self, x: int, y: int):
        result = True
        for window_x, window_y in self.windows_positions:
            for check_x, check_y in list(bresenham(x, y, window_x, window_y)):
                if self.grid[check_y][check_x].cell_type == CellType.Wall and (check_x, check_y) not in self.windows_positions:
                    result = False
                    break
        return result

    @staticmethod
    def dist(x1, y1, x2, y2) -> float:
        return ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5
