from copy import deepcopy
from threading import Thread, Lock
from typing import Optional

import pygame
from pygame.time import Clock

from intelligent_lights.display import Display
from intelligent_lights.visualization.visualization import Visualization
from intelligent_lights.visualization.visualization_context import VisualizationContext


class VisualizationManager:
    def __init__(self, width: int, height: int, grid_width: int, grid_height: int, status_bar_height=30, force_redraw: bool = False):
        self.height = height
        self.width = width
        self.grid_width = grid_width
        self.grid_height = grid_height
        self.status_bar_height = status_bar_height
        self.display = Display(self.width, self.height + status_bar_height, 'Intelligent lights')
        self.force_redraw = force_redraw
        self.cell_width = self.width // self.grid_width
        self.cell_height = self.height // self.grid_height

        self.visualization = Visualization(self.display, self.grid_width, self.grid_height, self.cell_width,
                                           self.cell_height, self.status_bar_height)
        self.draw_thread = Thread(target=self._draw_thread)
        self.context: Optional[VisualizationContext] = None
        self.context_modified: bool = True
        self.draw_mutex: Lock = Lock()
        self.running = True
        self.button_status = [False, False]

    def should_speed_down(self):
        if not self.button_status[0]:
            return False
        self.button_status[0] = False
        return True

    def should_speed_up(self):
        if not self.button_status[1]:
            return False
        self.button_status[1] = False
        return True

    def start(self):
        self._draw_thread()

    def redraw(self, context: VisualizationContext) -> None:
        with self.draw_mutex:
            self.context = context
            self.context_modified = True

    def _draw_thread(self) -> None:
        clock = Clock()
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = pygame.mouse.get_pos()
                    print("Pressed:", x // self.cell_width, y // self.cell_height)
                    if self.visualization.speed_down_button.collidepoint(x, y):
                        self.button_status[0] = True
                    if self.visualization.speed_up_button.collidepoint(x, y):
                        self.button_status[1] = True
                    if self.visualization.movement_button.collidepoint(x, y):
                        self.visualization.surface = "MOVEMENT"
                    if self.visualization.history_button.collidepoint(x, y):
                        self.visualization.surface = "HISTORY"
            redraw_context = None
            with self.draw_mutex:
                if self.context is not None and (self.context_modified or self.force_redraw):
                    redraw_context = deepcopy(self.context)
            if redraw_context:
                self.visualization.draw(redraw_context)
                self.context_modified = False
            clock.tick(20)
        pygame.quit()
