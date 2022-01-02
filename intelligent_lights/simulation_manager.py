from time import sleep, time
import random

from intelligent_lights.core.illuminance_calculator import IlluminanceCalculator
from intelligent_lights.lights_adjuster import LightsAdjuster
from intelligent_lights.person_simulator import PersonSimulator
from intelligent_lights.visualization.visualization_context import VisualizationContext
from intelligent_lights.visualization.visualization_manager import VisualizationManager


class SimulationManager:
    def __init__(self, vis_manager, grid, light_dict, sensors, cameras, rooms, sectors, cell_size, exits, windows,
                 persons, sun_power, sun_position, sun_distance, detection_points):
        self.windows = windows
        self.exits = exits
        self.cell_size = cell_size
        self.sectors = sectors
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
        self.lights_adjuster = LightsAdjuster()
        self.person_simulator = PersonSimulator(persons)
        self.illuminance_calc = IlluminanceCalculator()

    def run(self):
        sleep(0.5)
        self.draw()
        while self.visualization_manager.running:
            t = time()
            self.person_simulator.process(self.grid, self.cameras)
            should_light = self.get_enabled_points()
            sensors = set((x, y, self.grid[y][x].light_level) for x, y in self.sensors)
            self.lights_adjuster.process(sensors, self.lights, self.sectors, self.rooms, should_light)  # TODO

            self.draw()
            t = time() - t
            if t < 0.1:
                sleep(0.1 - t)

    def get_time(self) -> str:
        return "22:22"  # TODO

    def draw(self):
        persons_visible_positions, persons_not_visible_positions = self.person_simulator.get_persons_positions()
        ctx = VisualizationContext(self.grid, persons_visible_positions, persons_not_visible_positions, self.light_dict,
                                   set(self.sensors), set(self.cameras), self.sectors, self.exits, self.rooms,
                                   self.windows, self.cell_size, self.get_time(), self.sun_power, self.sun_position,
                                   self.sun_distance, set(self.detection_points))
        self.update_lights(ctx)
        self.visualization_manager.redraw(ctx)

    def get_enabled_points(self):
        persons, _ = self.person_simulator.get_persons_positions()
        result = {}
        for point in self.detection_points:
            sector = self.lights_adjuster.find_sector_for_cell(*point, self.sectors)
            result[point] = any(sector.is_cell_in(*pos) for pos in persons)
        return result

    def update_lights(self, context):
        for x in range(len(context.grid[0])):
            for y in range(len(context.grid)):
                context.grid[y][x].light_level = min(self.illuminance_calc.calculate(x, y, context), 255)
