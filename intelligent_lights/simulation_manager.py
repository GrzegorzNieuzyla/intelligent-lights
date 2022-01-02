from time import sleep

from intelligent_lights.core.illuminance_calculator import IlluminanceCalculator
from intelligent_lights.lights_adjuster import LightsAdjuster
from intelligent_lights.person_simulator import PersonSimulator
from intelligent_lights.visualization.visualization_context import VisualizationContext
from intelligent_lights.visualization.visualization_manager import VisualizationManager


class SimulationManager:
    def __init__(self, vis_manager, grid, lights, sensors, cameras, rooms, sectors, cell_size, exits, windows, persons, sun_power, sun_position, sun_distance):
        self.persons = persons
        self.windows = windows
        self.exits = exits
        self.cell_size = cell_size
        self.sectors = sectors
        self.rooms = rooms
        self.cameras = cameras
        self.sensors = sensors
        self.lights = lights
        self.sun_power = sun_power
        self.sun_position = sun_position
        self.sun_distance = sun_distance
        self.grid = grid
        self.visualization_manager: VisualizationManager = vis_manager
        self.lights_adjuster = LightsAdjuster()
        self.person_simulator = PersonSimulator()

    def run(self):
        sleep(0.5)
        while self.visualization_manager.running:
            self.person_simulator.process()  # TODO
            self.lights_adjuster.process()  # TODO

            ctx = VisualizationContext(self.grid, self.persons, self.lights, set(self.sensors), set(self.cameras),
                                       self.sectors, self.exits, self.rooms, self.windows, self.cell_size,
                                       self.get_time(), self.sun_power, self.sun_position, self.sun_distance)
            self.update_lights(ctx)
            self.visualization_manager.redraw(ctx)
            sleep(0.1)

    def get_time(self) -> str:
        return "22:22"  # TODO

    @staticmethod
    def update_lights(context):
        for x in range(len(context.grid[0])):
            for y in range(len(context.grid)):
                context.grid[y][x].light_level = min(IlluminanceCalculator.calculate(x, y, context), 255)
