import pygame
from pygame.locals import *


class TextBox:
    def __init__(self, x, y, width, surf):
        self.box = pygame.Rect(x, y, width, 100)
        pygame.draw.rect(surf, (255, 0, 0), self.box)
