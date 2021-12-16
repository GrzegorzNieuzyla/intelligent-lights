from random import randint

from intelligent_lights.parser import Parser
from intelligent_lights.visualization.visualization_manager import VisualizationManager
from intelligent_lights.visualization.visualization_context import VisualizationContext

parser = Parser("floor.json")

SAMPLE_GRID = parser.grids["Floor 1"]
SAMPLE_LIGHTS = parser.lights["Floor 1"]

SAMPLE_PERSONS = {
    (1, 1),
    (20, 20),
    (70, 20),
    (22, 40),
    (50, 30),
    (90, 40),
}

visualization = VisualizationManager(1600, 900, len(SAMPLE_GRID[0]), len(SAMPLE_GRID), force_redraw=True)

for light in SAMPLE_LIGHTS:
    light.light_level = randint(0, 100)
    SAMPLE_GRID[light.y][light.x].light_level = light.light_level

for x, row in enumerate(SAMPLE_GRID):
    for y, cell in enumerate(row):
        cell.light_level = 100 * (y + x) / (len(SAMPLE_GRID[0]) + len(SAMPLE_GRID))

light_dict = {(light.x, light.y): light for light in SAMPLE_LIGHTS}
vis_context = VisualizationContext(SAMPLE_GRID, SAMPLE_PERSONS, light_dict, "22:22")

visualization.redraw(vis_context)
