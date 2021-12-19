from math import sqrt, floor

from intelligent_lights.cells.cell_type import CellType
from intelligent_lights.visualization.visualization_context import VisualizationContext


class IlluminanceCalculator:
    power_multiplier = 8e4

    def __init__(self):
        pass

    '''
    E = I*cos(alfa)/r^2
    '''
    @staticmethod
    def calculate(x: int, y: int, context: VisualizationContext):
        h = 200
        cell_size = 20
        E = 0
        for x_light, y_light in context.light_positions:
            if IlluminanceCalculator.is_wall_in_straight_line(x, y, x_light, y_light, context):
                continue
            dx = (x - x_light) * cell_size
            dy = (y - y_light) * cell_size
            d = sqrt(dx ** 2 + dy ** 2)
            r = sqrt(d ** 2 + h ** 2)
            I = context.light_positions[(x_light, y_light)].light_level * IlluminanceCalculator.power_multiplier
            cos_alfa = h / r
            E += I * cos_alfa / r ** 2

        return round(E)

    @staticmethod
    def is_wall_in_straight_line(x1: int, y1: int, x2: int, y2: int, context: VisualizationContext):
        line = []

        if x2 - x1 != 0:
            a = round((y2 - y1) / (x2 - x1), 3)
            b = round(-x1 * (y2 - y1) / (x2 - x1) + y1, 3)
        else:
            a = 1e12
            b = 1e12

        if abs(a) > 1 and a != 1e12:
            for y in range(min(y1, y2) + 1, max(y1, y2)):
                x = floor((y - b) / a)
                line.append((x, y))
        if a == 0:
            for x in range(min(x1, x2) + 1, max(x1, x2)):
                line.append((x, y1))
        if a == 1e12:
            for y in range(min(y1, y2) + 1, max(y1, y2)):
                line.append((x1, y))
        if abs(a) <= 1:
            for x in range(min(x1, x2) + 1, max(x1, x2)):
                y = floor(a * x + b)
                line.append((x, y))

        for p in line:
            x, y = p
            if context.grid[y][x].cell_type == CellType.Wall:
                return True

        return False
