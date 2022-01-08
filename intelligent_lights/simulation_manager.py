from time import sleep, time

from intelligent_lights.core.illuminance_calculator import IlluminanceCalculator
from intelligent_lights.lights_adjuster import LightsAdjuster
from intelligent_lights.person_simulator import PersonSimulator
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
        self.cameras = cameras
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
        self.person_simulator = PersonSimulator(persons)
        self.illuminance_calc = IlluminanceCalculator()

    def run(self):
        sleep(0.5)
        self.update_environment_and_draw()
        while self.visualization_manager.running:
            t = time()
            self.person_simulator.process(self.grid, self.cameras)
            should_light = self.get_enabled_points()
            self.update_sensors()
            self.lights_adjuster.process(should_light)  # TODO
            self.update_environment_and_draw()
            t = time() - t
            if t < self.MIN_FRAME_DELAY:
                sleep(self.MIN_FRAME_DELAY - t)

    def get_time(self) -> str:
        return "22:22"  # TODO

    def update_environment_and_draw(self):
        persons_visible_positions, persons_not_visible_positions = self.person_simulator.get_persons_positions()
        ctx = VisualizationContext(self.grid, persons_visible_positions, persons_not_visible_positions, self.light_dict,
                                   set(map(lambda s: (s.x, s.y), self.sensors)), set(self.cameras), self.exits,
                                   self.rooms, self.windows, self.cell_size, self.get_time(), self.sun_power,
                                   self.sun_position, self.sun_distance, set(self.detection_points))
        self.update_lights(ctx)
        self.visualization_manager.redraw(ctx)

    def get_enabled_points(self):
        persons, _ = self.person_simulator.get_persons_positions()
        result = {p: False for p in self.detection_points}

        for person in persons:
            room = self.lights_adjuster.find_room_for_cell(*person)
            if not room: continue
            points_in_room = list(filter(lambda p: room.is_cell_in(*p), self.detection_points))
            points_with_dist = {p: self.lights_adjuster.dist(*person, *p) for p in points_in_room}
            min_dist = min(points_with_dist.values())
            dist_epsilon = 5
            points = list(filter(lambda l: points_with_dist[l] <= min_dist + dist_epsilon, points_with_dist.keys()))
            for point in points:
                result[point] = True

        return result

    def update_lights(self, context):
        for x in range(len(context.grid[0])):
            for y in range(len(context.grid)):
                context.grid[y][x].light_level = min(self.illuminance_calc.calculate(x, y, context), 255)

    def update_sensors(self):
        for sensor in self.sensors:
            sensor.value = self.grid[sensor.y][sensor.x].light_level
