from typing import Set, List, Tuple, Dict

from intelligent_lights.cells.room import Room
from intelligent_lights.light import Light
from intelligent_lights.sensors import Sensor


class LightsAdjuster:
    EPSILON = 5
    REQUIRED_LIGHT = 100
    MAX_SENSOR_DISTANCE = 5
    HYSTERESIS_TIME = 20
    HYSTERESIS_DELAY = 10

    def __init__(self, sensors: Set[Sensor], lights: List[Light], rooms: List[Room],
                 detection_points: List[Tuple[int, int]], cell_size: float, time_step):
        self.to_adjust = {}
        self.applicable_lights = {}
        self.applicable_sensors = {}
        self.lights_mapping = {}
        self.adjusted_lights = {}
        self.lights_to_fade = {}
        self.sensors = sensors
        self.lights = lights
        self.rooms = rooms
        self.cell_size = cell_size
        self.detection_points = detection_points
        self.sensor_distance = self.MAX_SENSOR_DISTANCE / self.cell_size
        self.time_step = time_step
        self.preprocess()
        self._time = 0

    def preprocess(self):
        for detection_point in self.detection_points:
            self.applicable_lights[detection_point] = self.find_applicable_lights(detection_point)
            self.applicable_sensors[detection_point] = self.find_applicable_sensors(detection_point)
        for light in self.lights:
            self.lights_mapping[light] = list(filter(lambda p: light in self.applicable_lights[p], self.detection_points))

    def process(self, should_light: Dict[Tuple[int, int], bool]):

        for detection_point in self.filter_detection_points(should_light):
            applicable_lights = self.find_applicable_lights(detection_point)
            sensors_to_adjust = self.find_applicable_sensors(detection_point)
            value = self._calculate_light_value(*detection_point, sensors=sensors_to_adjust)
            self.lights_to_fade = {l: t for l, t in self.lights_to_fade.items() if l not in applicable_lights}

            if value < self.REQUIRED_LIGHT:
                if detection_point in self.to_adjust:
                    ratio = max(0, value - self.to_adjust[detection_point]) / self.EPSILON
                    if ratio == 0:
                        # light is max value
                        prev = len(self.applicable_lights[detection_point])
                        self.applicable_lights[detection_point] = self.find_applicable_lights(detection_point, search_again=True)
                        if prev == len(self.applicable_lights[detection_point]):
                            # no more lights to control
                            del self.to_adjust[detection_point]
                        continue
                    req = (self.REQUIRED_LIGHT + self.EPSILON - value) / ratio
                    if req <= 0:
                        continue
                    for light in applicable_lights:
                        light.light_level = min(req + light.light_level, Light.MAX_VALUE)
                    del self.to_adjust[detection_point]
                    del self.adjusted_lights[detection_point]
                else:
                    lights = set()
                    for light in applicable_lights:
                        if any(light in light_set for light_set in self.adjusted_lights.values()):
                            continue
                        light.light_level += self.EPSILON
                        lights.add(light)
                    if lights:
                        self.to_adjust[detection_point] = value
                        self.adjusted_lights[detection_point] = lights

            elif detection_point in self.to_adjust:
                del self.to_adjust[detection_point]

        self.turn_off_unnecessary_lights(should_light)
        self.fade_out_lights()
        self._time += self.time_step

    @staticmethod
    def filter_detection_points(should_light: Dict[Tuple[int, int], bool], on: bool = True) -> List[Tuple[int, int]]:
        return list(map(lambda p: p[0], filter(lambda x_: on == x_[1], should_light.items())))

    def find_applicable_lights(self, detection_point: Tuple[int, int], search_again=False) -> List[Light]:
        if detection_point in self.applicable_lights and not search_again:
            return self.applicable_lights[detection_point]

        dist_epsilon = 4
        while True:
            room = self.find_room_for_cell(*detection_point)
            lights_in_room = list(filter(lambda p: room.is_cell_in(p.x, p.y), self.lights))
            lights_with_dist = {l: self.dist(*detection_point, l.x, l.y) for l in lights_in_room}
            min_dist = min(lights_with_dist.values())
            result = list(filter(lambda l: lights_with_dist[l] <= min_dist + dist_epsilon, lights_with_dist.keys()))
            self.applicable_lights[detection_point] = result
            if not search_again or len(self.applicable_lights[detection_point]) == len(lights_in_room) or len(
                    self.applicable_lights) < len(result):
                break
            dist_epsilon += 4

        return result

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
                filter(lambda s: self.dist(s.x, s.y, *detection_point) <= self.sensor_distance, sensors_in_room))

        self.applicable_sensors[detection_point] = sensors_to_adjust
        return sensors_to_adjust

    def turn_off_unnecessary_lights(self, should_light):
        self.to_adjust = {k: v for k, v in self.to_adjust.items() if should_light[k]}
        self.adjusted_lights = {k: v for k, v in self.adjusted_lights.items() if should_light[k]}

        for light in self.lights:
            if all(not should_light[p] for p in self.lights_mapping[light]):
                if light not in self.lights_to_fade:
                    self.lights_to_fade[light] = self._time + self.HYSTERESIS_DELAY

    def fade_out_lights(self):
        try:
            val = Light.MAX_VALUE / (self.HYSTERESIS_TIME / self.time_step)
        except ZeroDivisionError:
            val = Light.MAX_VALUE

        for light, t in self.lights_to_fade.items():
            if self._time >= t:
                light.light_level = max(0, light.light_level - val)
        self.lights_to_fade = {l: v for l, v in self.lights_to_fade.items() if l.light_level > 0}

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

    @staticmethod
    def dist(x1, y1, x2, y2) -> float:
        return ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5
