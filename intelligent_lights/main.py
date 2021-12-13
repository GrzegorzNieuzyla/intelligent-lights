from intelligent_lights.sample_grid import SAMPLE_GRID, SAMPLE_LIGHTS, SAMPLE_PERSONS
from intelligent_lights.visualization import Visualization
from intelligent_lights.visualization_context import VisualizationContext

visualization = Visualization(len(SAMPLE_GRID[0]), len(SAMPLE_GRID))


for light in SAMPLE_LIGHTS:
    SAMPLE_GRID[light.y][light.x].light_level = light.light_level

vis_context = VisualizationContext(SAMPLE_GRID, SAMPLE_PERSONS, "22:22")

visualization.redraw(vis_context)
