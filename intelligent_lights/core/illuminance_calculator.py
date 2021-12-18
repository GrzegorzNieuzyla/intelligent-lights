import numpy as np
from math import sqrt, floor

from intelligent_lights.cells.wall import Wall
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
            # if IlluminanceCalculator.is_wall_in_straight_line(x, y, y_light, x_light, context):
            #     continue
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
        xx = [x1, x2]
        yy = [y1, y2]
        coeff = np.polyfit(xx, yy, 1)
        a = round(coeff[0], 3)
        b = round(coeff[1], 3)
        if abs(a) > 1:
            for y in range(min(y1, y2), max(y1, y2)):
                x = floor((y - b) / a)
                line.append((x, y))
        elif a == 0:
            for x in range(min(x1, x2), max(x1, x2)):
                line.append((x, x + 1))
        else:
            for x in range(min(x1, x2), max(x1, x2)):
                y = floor(a * x + b)
                line.append((x, y))
        for p in line:
            x = p[0]
            y = p[1]
            if isinstance(context.grid[x][y], Wall):
                return True

        return False
