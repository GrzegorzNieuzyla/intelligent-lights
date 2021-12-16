import pygame


class Display:
    def __init__(self, width, height, title=' '):
        pygame.init()
        pygame.display.set_caption(title)
        pygame.font.init()
        self.width = width
        self.height = height
        self.window = pygame.display.set_mode((width, height), pygame.DOUBLEBUF)
