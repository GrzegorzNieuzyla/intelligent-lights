from threading import Thread

from intelligent_lights.persons.person import Person
from intelligent_lights.parser import Parser
from intelligent_lights.sensors import Sensor
from intelligent_lights.simulation_manager import SimulationManager
from intelligent_lights.visualization.visualization_manager import VisualizationManager


def main(filename):
    parser = Parser(filename)

    SAMPLE_GRID = parser.grids["Floor 1"]
    SAMPLE_LIGHTS = parser.lights["Floor 1"]
    SAMPLE_SENSORS = set(map(lambda s: Sensor(*s), parser.sensors["Floor 1"]))
    SAMPLE_CAMERAS = parser.cameras["Floor 1"]
    SAMPLE_ROOMS = parser.rooms["Floor 1"]
    CELL_SIZE = parser.cell_sizes["Floor 1"]
    SAMPLE_EXITS = parser.exits["Floor 1"]
    SAMPLE_WINDOWS = parser.windows["Floor 1"]
    SAMPLE_SUN_POWER = parser.sun_power["Floor 1"]
    SAMPLE_SUN_POSITION = parser.sun_position["Floor 1"]
    SAMPLE_SUN_DISTANCE = parser.sun_distance["Floor 1"]
    SAMPLE_DETECTION_POINTS = parser.detection_points["Floor 1"]
    SAMPLE_PERSONS = [
        Person(SAMPLE_GRID, SAMPLE_ROOMS),
        Person(SAMPLE_GRID, SAMPLE_ROOMS),
        Person(SAMPLE_GRID, SAMPLE_ROOMS),
        Person(SAMPLE_GRID, SAMPLE_ROOMS),
        Person(SAMPLE_GRID, SAMPLE_ROOMS),
        Person(SAMPLE_GRID, SAMPLE_ROOMS),
        Person(SAMPLE_GRID, SAMPLE_ROOMS),
        Person(SAMPLE_GRID, SAMPLE_ROOMS),
        Person(SAMPLE_GRID, SAMPLE_ROOMS),
        Person(SAMPLE_GRID, SAMPLE_ROOMS)
    ]

    visualization = VisualizationManager(1600, 900, len(SAMPLE_GRID[0]), len(SAMPLE_GRID), force_redraw=True)

    for light in SAMPLE_LIGHTS:
        light.light_level = 0
        SAMPLE_GRID[light.y][light.x].light_level = light.light_level

    light_dict = {(light.x, light.y): light for light in SAMPLE_LIGHTS}

    simulator = SimulationManager(visualization, SAMPLE_GRID, light_dict, SAMPLE_SENSORS, SAMPLE_CAMERAS, SAMPLE_ROOMS,
                                  CELL_SIZE, SAMPLE_EXITS, SAMPLE_WINDOWS, SAMPLE_PERSONS, SAMPLE_SUN_POWER,
                                  SAMPLE_SUN_POSITION, SAMPLE_SUN_DISTANCE, SAMPLE_DETECTION_POINTS)

    sim_thread = Thread(target=simulator.run)
    sim_thread.start()
    visualization.start()


if __name__ == '__main__':
    main("floor.json")
