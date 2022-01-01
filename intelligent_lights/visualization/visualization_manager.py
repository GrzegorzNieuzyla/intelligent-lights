from copy import deepcopy
from threading import Thread, Lock
from typing import Optional

import pygame
from pygame.time import Clock

from intelligent_lights.display import Display
from intelligent_lights.visualization.visualization import Visualization
from intelligent_lights.visualization.visualization_context import VisualizationContext


class VisualizationManager:
    def __init__(self, width: int, height: int, grid_width: int, grid_height: int, force_redraw: bool = False):
        self.height = height
        self.width = width
        self.grid_width = grid_width
        self.grid_height = grid_height
        self.display = Display(self.width, self.height, 'Intelligent lights')
        self.force_redraw = force_redraw
        self.cell_width = self.width // self.grid_width
        self.cell_height = self.height // self.grid_height

        self.visualization = Visualization(self.display, self.grid_width, self.grid_height, self.cell_width,
                                           self.cell_height)
        self.draw_thread = Thread(target=self._draw_thread)
        self.context: Optional[VisualizationContext] = None
        self.context_modified: bool = True
        self.draw_mutex: Lock = Lock()
        self.running = True
        self.draw_thread.start()

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
                if event.type == pygame.MOUSEBUTTONUP:
                    x, y = pygame.mouse.get_pos()
                    print("Pressed:", x // self.cell_width, y // self.cell_height)

            redraw_context = None
            with self.draw_mutex:
                if self.context is not None and (self.context_modified or self.force_redraw):
                    redraw_context = deepcopy(self.context)
            if redraw_context:
                self.visualization.draw(redraw_context)
                self.context_modified = False
            clock.tick(20)
        pygame.quit()
