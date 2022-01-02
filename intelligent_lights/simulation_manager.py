from time import sleep, time
import random

from intelligent_lights.core.illuminance_calculator import IlluminanceCalculator
from intelligent_lights.lights_adjuster import LightsAdjuster
from intelligent_lights.person_simulator import PersonSimulator
from intelligent_lights.visualization.visualization_context import VisualizationContext
from intelligent_lights.visualization.visualization_manager import VisualizationManager


class SimulationManager:
    def __init__(self, vis_manager, grid, light_dict, sensors, cameras, rooms, sectors, cell_size, exits, windows, persons, sun_power, sun_position, sun_distance):
        self.persons = persons
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
        self.visualization_manager: VisualizationManager = vis_manager
        self.lights_adjuster = LightsAdjuster()
        self.person_simulator = PersonSimulator()
        self.illuminance_calc = IlluminanceCalculator()

    def run(self):
        sleep(0.5)
        while self.visualization_manager.running:
            t = time()
            self.person_simulator.process()  # TODO
            should_light = {l: random.random() > 0.1 for l in self.sensors}
            self.lights_adjuster.process(self.sensors, self.lights, self.sectors, self.rooms, should_light)  # TODO

            ctx = VisualizationContext(self.grid, self.persons, self.light_dict, set(self.sensors), set(self.cameras),
                                       self.sectors, self.exits, self.rooms, self.windows, self.cell_size,
                                       self.get_time(), self.sun_power, self.sun_position, self.sun_distance)
            self.update_lights(ctx)
            self.visualization_manager.redraw(ctx)
            t = time() - t
            if t < 0.1:
                sleep(0.1 - t)

    def get_time(self) -> str:
        return "22:22"  # TODO

    def update_lights(self, context):
        for x in range(len(context.grid[0])):
            for y in range(len(context.grid)):
                context.grid[y][x].light_level = min(self.illuminance_calc.calculate(x, y, context), 255)
                # context.grid[y][x].light_level = min(IlluminanceCalculator.calculate(x, y, context), 255)
                # context.grid[y][x].light_level = min(random.randint(0, 255), 255)
