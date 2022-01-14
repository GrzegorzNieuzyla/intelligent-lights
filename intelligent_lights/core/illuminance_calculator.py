from copy import copy
from math import floor

from intelligent_lights.cells.cell_type import CellType
from intelligent_lights.visualization.visualization_context import VisualizationContext
from intelligent_lights.light import Light


class IlluminanceCalculator:
    power_multiplier = 20

    def __init__(self, blinds_adjuster):
        self.cache = {}
        self.blinds_adjuster = blinds_adjuster

    '''
    E = I*cos(alfa)/r^2
    '''
    def calculate(self, x: int, y: int, context: VisualizationContext):
        # h = 200
        cell_size = context.cell_size_in_meter
        E = 0
        all_lights = copy(context.light_positions)
        for p in context.sun_position:
            all_lights[(p, -context.sun_distance)] = Light(p, -context.sun_distance, context.sun_power)

        for x_light, y_light in all_lights:
            if self.is_wall_in_straight_line(x, y, x_light, y_light, context):
                continue
            dx = (x - x_light) * cell_size
            dy = (y - y_light) * cell_size
            # d = sqrt(dx ** 2 + dy ** 2)
            # r = sqrt(d ** 2 + h ** 2)
            r = dx ** 2 + dy ** 2
            if r == 0:
                continue
            I = all_lights[(x_light, y_light)].light_level * IlluminanceCalculator.power_multiplier
            # cos_alfa = h / r
            if x_light < 0 or y_light < 0:
                E += I / IlluminanceCalculator.power_multiplier * self.blinds_adjuster.level
            else:
                E += I / r

        return round(E)

    def is_wall_in_straight_line(self, x1: int, y1: int, x2: int, y2: int, context: VisualizationContext):
        if (x1, y1, x2, y2) in self.cache:
            return self.cache[(x1, y1, x2, y2)]
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

        result = False

        for p in line:
            x, y = p
            if x < 0 or y < 0:
                continue
            windows = []
            for w in context.windows:
                b = w.bounds
                if b[0] == 0:
                    for i in range(b[3]):
                        windows.append((0, b[1] + i))
                if b[1] == 0:
                    for i in range(b[2]):
                        windows.append((b[0] + i, 0))

            if x >= 100 or y >= 50:
                continue

            if context.grid[y][x].cell_type == CellType.Wall and (x, y) not in windows:
                result = True
                break

        self.cache[(x1, y1, x2, y2)] = result
        return result
