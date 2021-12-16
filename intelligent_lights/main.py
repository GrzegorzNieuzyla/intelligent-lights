from intelligent_lights.sample_grid import SAMPLE_GRID, SAMPLE_LIGHTS, SAMPLE_PERSONS
from intelligent_lights.visualization.visualization_manager import VisualizationManager
from intelligent_lights.visualization.visualization_context import VisualizationContext

visualization = VisualizationManager(1600, 900, len(SAMPLE_GRID[0]), len(SAMPLE_GRID), force_redraw=True)

for light in SAMPLE_LIGHTS:
    SAMPLE_GRID[light.y][light.x].light_level = light.light_level

for x, row in enumerate(SAMPLE_GRID):
    for y, cell in enumerate(row):
        cell.light_level = 100 * (y + x) / (len(SAMPLE_GRID[0]) + len(SAMPLE_GRID))


light_dict = {(light.x, light.y): light for light in SAMPLE_LIGHTS }
vis_context = VisualizationContext(SAMPLE_GRID, SAMPLE_PERSONS, light_dict, "22:22")

visualization.redraw(vis_context)
