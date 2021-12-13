import pygame.event
from pygame.time import Clock

from display import Display

display = Display(1600, 900, "Intelligent lights")
clock = Clock()

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            running = False
        pygame.display.flip()
        clock.tick(60)
