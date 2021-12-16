from typing import Tuple, List

import pygame

from intelligent_lights.cells.cell_type import CellType
from intelligent_lights.display import Display
from intelligent_lights.visualization.visualization_context import VisualizationContext

BACKGROUND_COLOR = (255, 255, 255)
WALL_COLOR = (0, 0, 96)
PERSON_COLOR = (255, 0, 0)
EMPTY_COLOR = (255, 255, 0)
DEVICE_COLOR = (176, 0, 176)
LIGHT_COLOR = (255, 255, 255)
TEXT_COLOR = (255, 0, 0)


class Visualization:
    def __init__(self, display: Display, width: int, height: int, cell_width: int, cell_height: int):
        self.display: Display = display
        self.cell_width = cell_width
        self.cell_height = cell_height
        self.width = width
        self.height = height
        self.screen = self.display.window
        self.font = pygame.font.SysFont("monospace", int(self.cell_height / 1.5), bold=True)

    def get_cells(self) -> List[Tuple[int, int, int, int]]:
        for x in range(self.width):
            for y in range(self.height):
                yield x, y, *self.get_screen_position(x, y)

    def get_screen_position(self, x, y):
        return x * self.cell_width, y * self.cell_height

    @staticmethod
    def get_light_value(value) -> Tuple[int, int, int]:
        val = 10 + value * 2.5
        return val, val, 0

    def draw_text(self, text, x, y):
        surface = self.font.render(text, False, TEXT_COLOR)
        rect = surface.get_rect(center=(x, y))
        self.screen.blit(surface, rect)

    def get_center(self, x, y):
        return x + self.cell_width // 2, y + self.cell_height // 2

    def draw(self, context: VisualizationContext):
        self.screen.fill(BACKGROUND_COLOR)
        for grid_x, grid_y, x, y in self.get_cells():
            cell = context.grid[grid_y][grid_x]

            color = BACKGROUND_COLOR
            if cell.cell_type == CellType.Wall:
                color = WALL_COLOR
            elif cell.cell_type == CellType.Empty:
                color = self.get_light_value(cell.light_level)
            elif cell.cell_type == CellType.Device:
                color = DEVICE_COLOR
            if (grid_x, grid_y) in context.light_positions:
                color = LIGHT_COLOR
            pygame.draw.rect(self.screen, color, pygame.Rect(x, y, self.cell_width, self.cell_height))
            if (grid_x, grid_y) in context.person_positions:
                pygame.draw.circle(self.screen, PERSON_COLOR, self.get_center(x, y),
                                   min(self.cell_width, self.cell_height) // 2)

        for grid_x, grid_y in context.light_positions:
            self.draw_text(str(int(context.light_positions[(grid_x, grid_y)].light_level)),
                           *self.get_center(*self.get_screen_position(grid_x, grid_y)))

        pygame.display.flip()
