from typing import Tuple, List

import pygame

from intelligent_lights.cells.cell_type import CellType
from intelligent_lights.display import Display
from intelligent_lights.visualization.visualization_context import VisualizationContext

BACKGROUND_COLOR = (255, 255, 255)
WALL_COLOR = (0, 0, 96)
PERSON_BLUE_COLOR = (0, 0, 255)
PERSON_RED_COLOR = (255, 0, 0)
EMPTY_COLOR = (255, 255, 0)
DEVICE_COLOR = (176, 0, 176)
LIGHT_COLOR = (255, 255, 255)
TEXT_COLOR = (255, 0, 0)
CAMERA_COLOR = (128, 128, 128)
SENSOR_COLOR = (255, 128, 0)
SECTOR_COLOR = (255, 0, 0)
EXIT_COLOR = (0, 255, 0)
ROOM_COLOR = (176, 0, 176)
WINDOW_COLOR = (0, 0, 255)
DETECTION_POINT = (0, 128, 0)


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
    def get_light_value(cell) -> Tuple[int, int, int]:
        val = max(0, min(cell.light_level, 255))
        return val, val, 0

    def draw_text(self, text, x, y, color=TEXT_COLOR):
        surface = self.font.render(text, False, color)
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
                color = self.get_light_value(context.grid[grid_y][grid_x])
            elif cell.cell_type == CellType.Device:
                color = DEVICE_COLOR
            if (grid_x, grid_y) in context.light_positions:
                color = LIGHT_COLOR
            pygame.draw.rect(self.screen, color, pygame.Rect(x, y, self.cell_width, self.cell_height))
            if (grid_x, grid_y) in context.person_visible_positions:
                pygame.draw.circle(self.screen, PERSON_BLUE_COLOR, self.get_center(x, y),
                                   min(self.cell_width, self.cell_height) // 2)
            if (grid_x, grid_y) in context.person_not_visible_positions:
                pygame.draw.circle(self.screen, PERSON_RED_COLOR, self.get_center(x, y),
                                   min(self.cell_width, self.cell_height) // 2)
            if (grid_x, grid_y) in context.camera_positions:
                pygame.draw.circle(self.screen, CAMERA_COLOR, self.get_center(x, y),
                                   min(self.cell_width, self.cell_height) // 2)
            if (grid_x, grid_y) in context.sensor_positions:
                pygame.draw.circle(self.screen, SENSOR_COLOR, self.get_center(x, y),
                                   min(self.cell_width, self.cell_height) // 2)
            if (grid_x, grid_y) in context.detection_points:
                pygame.draw.circle(self.screen, DETECTION_POINT, self.get_center(x, y),
                                   min(self.cell_width, self.cell_height) // 2)

        for grid_x, grid_y in context.light_positions:
            self.draw_text(str(int(context.light_positions[(grid_x, grid_y)].light_level)),
                           *self.get_center(*self.get_screen_position(grid_x, grid_y)))

        for sector in context.sectors:
            x, y, w, h = sector.bounds
            x, y = self.get_screen_position(x, y)
            w *= self.cell_width
            h *= self.cell_height
            pygame.draw.rect(self.screen, SECTOR_COLOR, pygame.Rect(x, y, w, h), width=2)

        for ex in context.exits:
            x, y, w, h = ex.bounds
            x, y = self.get_screen_position(x, y)
            w *= self.cell_width
            h *= self.cell_height
            pygame.draw.rect(self.screen, EXIT_COLOR, pygame.Rect(x, y, w, h), width=2)

        for w in context.windows:
            x, y, w, h = w.bounds
            x, y = self.get_screen_position(x, y)
            w *= self.cell_width
            h *= self.cell_height
            pygame.draw.rect(self.screen, WINDOW_COLOR, pygame.Rect(x, y, w, h))

        for room in context.rooms:
            for rect in room.rects:
                x, y, w, h = rect
                x, y = self.get_screen_position(x, y)
                w *= self.cell_width
                h *= self.cell_height
                pygame.draw.rect(self.screen, ROOM_COLOR, pygame.Rect(x, y, w, h), width=2)
                self.draw_text(room.label, x + w // 2, y + h // 2, ROOM_COLOR)

        pygame.display.flip()
