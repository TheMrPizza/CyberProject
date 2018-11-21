import pygame
from pygame.locals import *
import sys
import threading

world = None


class World:
    def __init__(self):  # Hello World!
        self.SIZE = (640, 480)
        self.SURF = None
        self.FPS = 30
        self.cur_screen = None
        self.clock = pygame.time.Clock()
        self.loop_thread = None

    def set_screen(self):
        pygame.init()
        self.SURF = pygame.display.set_mode(self.SIZE)
        pygame.display.set_caption("Cyber!")
        self.world_loop()

    def world_loop(self):
        from Login import Login
        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()

            self.cur_screen = Login()

            pygame.display.update()
            self.clock.tick(self.FPS)

    def draw_rect(self, rect, rect_color):
        pygame.draw.rect(self.SURF, rect_color, rect)


def main():
    global world
    world = World()
    world.loop_thread = threading.Thread(target=world.set_screen)
    world.loop_thread.start()

if __name__ == '__main__':
    main()
