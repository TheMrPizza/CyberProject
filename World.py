import pygame
from pygame.locals import *


class World:
    def __init__(self):  # Hello World!
        self.SIZE = (640, 480)
        self.SURF = pygame.display.set_mode(self.SIZE)
        self.cur_screen = None
