import pygame
from pygame.locals import *
import sys
import TextBox

pygame.init()
DISPLAY_SURF = pygame.display.set_mode((640, 480))
pygame.display.set_caption("Cyber!")
tb = TextBox.TextBox(100, 100, 300, DISPLAY_SURF)

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    pygame.display.update()
