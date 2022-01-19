from datetime import datetime, timedelta
from time import sleep, time

from intelligent_lights.camera_simulator import CameraSimulator
from intelligent_lights.core.illuminance_calculator import IlluminanceCalculator
from intelligent_lights.lights_adjuster import LightsAdjuster
from intelligent_lights.blinds_adjuster import BlindsAdjuster
from intelligent_lights.person_simulator import PersonSimulator
from intelligent_lights.sun_simulator import SunSimulator
from intelligent_lights.visualization.visualization_context import VisualizationContext
from intelligent_lights.visualization.visualization_manager import VisualizationManager


class SimulationManager:
    TIME_STEP_IN_S = 0.5
    MIN_FRAME_DELAY = 0.1

    def __init__(self, vis_manager, grid, light_dict, sensors, cameras, rooms, cell_size, exits, windows,
                 persons, sun_power, sun_position, sun_distance, detection_points):
        self.windows = windows
        self.exits = exits
        self.cell_size = cell_size
        self.rooms = rooms
        self.sensors = sensors
        self.light_dict = light_dict
        self.lights = list(self.light_dict.values())
        self.sun_power = sun_power
        self.sun_position = sun_position
        self.sun_distance = sun_distance
        self.grid = grid
        self.detection_points = detection_points
        self.visualization_manager: VisualizationManager = vis_manager
        self.lights_adjuster = LightsAdjuster(self.sensors, self.lights, self.rooms, self.detection_points,
                                              self.cell_size, self.TIME_STEP_IN_S)
        self.blinds_adjuster = BlindsAdjuster(self.detection_points, self.rooms, self.sensors, self.windows, self.grid, self.cell_size)
        self.sun_simulator = SunSimulator(sun_power, sun_position)
        self.person_simulator = PersonSimulator(persons)
        self.camera_simulator = CameraSimulator(cameras)
        self.illuminance_calc = IlluminanceCalculator(self.blinds_adjuster)
        self._time = datetime(2022, 2, 22, 10, 00)
        self.step = 0
        self.redraw_interval = 1
        self.current_speed = 0
        self.speeds = [1, 2, 5, 10, 20, 60, 120, 240]

    def run(self):
        sleep(0.5)
        self.update_environment_and_draw()
        t = 0
        while self.visualization_manager.running:
            t = time()
            if self.should_redraw():
                t = time()

            self.update_speed()
            self.update_sun()
            self.person_simulator.process(self.grid)
            self.camera_simulator.process(self.grid, self.person_simulator.persons)
            should_light = self.get_enabled_points()
            self.update_sensors()
            self.blinds_adjuster.process()
            self.lights_adjuster.process(should_light)  # TODO
            self.update_environment_and_draw()
            self._time += timedelta(seconds=self.TIME_STEP_IN_S)

            self.step += 1
            if self.should_redraw():
                t = time() - t
                if t < self.MIN_FRAME_DELAY:
                    sleep(self.MIN_FRAME_DELAY - t)

    def get_time(self) -> str:
        return f"{self._time.hour:02}:{self._time.minute:02}:{self._time.second:02}"

    def update_environment_and_draw(self):
        persons_visible_positions, persons_not_visible_positions, _ = self.person_simulator.get_persons_positions()
        ctx = VisualizationContext(self.grid, persons_visible_positions, persons_not_visible_positions, self.light_dict,
                                   set(map(lambda s: (s.x, s.y), self.sensors)), set(self.camera_simulator.cameras), self.exits,
                                   self.rooms, self.windows, self.cell_size, self.get_time(), self.sun_power,
                                   self.sun_position, self.sun_distance, set(self.detection_points), self.get_secs_per_frame())
        self.update_lights(ctx)
        if self.should_redraw():
            self.visualization_manager.redraw(ctx)

    def get_secs_per_frame(self):
        return f"{self.redraw_interval * self.TIME_STEP_IN_S} sec/frame"

    def get_enabled_points(self):
        persons, _, predictions = self.person_simulator.get_persons_positions()
        result = {p: False for p in self.detection_points}

        for position in set.union(persons, predictions):
            room = self.lights_adjuster.find_room_for_cell(*position)
            if not room: continue
            points_in_room = list(filter(lambda p: room.is_cell_in(*p), self.detection_points))
            points_with_dist = {p: self.lights_adjuster.dist(*position, *p) for p in points_in_room}
            min_dist = min(points_with_dist.values())
            dist_epsilon = 5
            points = list(filter(lambda l: points_with_dist[l] <= min_dist + dist_epsilon, points_with_dist.keys()))
            for point in points:
                result[point] = True

        return result

    def update_lights(self, context):
        if not self.should_redraw():
            for x, y in context.sensor_positions:
                context.grid[y][x].light_level = min(self.illuminance_calc.calculate(x, y, context), 255)
            return

        for x in range(len(context.grid[0])):
            for y in range(len(context.grid)):
                context.grid[y][x].light_level = min(self.illuminance_calc.calculate(x, y, context), 255)

    def update_sensors(self):
        for sensor in self.sensors:
            sensor.value = self.grid[sensor.y][sensor.x].light_level

    def update_speed(self):
        if self.visualization_manager.should_speed_down():
            self.current_speed = max(0, self.current_speed - 1)
        if self.visualization_manager.should_speed_up():
            self.current_speed = min(len(self.speeds) - 1, self.current_speed + 1)
        self.redraw_interval = self.speeds[self.current_speed]

    def should_redraw(self):
        return self.step % self.redraw_interval == 0
    
    def update_sun(self):
        self.sun_simulator.process()
        self.sun_power = self.sun_simulator.sun_power
        self.sun_position = self.sun_simulator.sun_position

