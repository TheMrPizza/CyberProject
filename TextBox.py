import World
import pygame
from pygame.locals import *


class TextBox:
    def __init__(self, x, y, width):
        self.box = pygame.Rect(x, y, width, 100)
        print World.world.SURF
        World.world.draw_rect(self.box, (255, 0, 0))
