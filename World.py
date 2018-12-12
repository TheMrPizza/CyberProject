import pygame
import sys
import threading


class World(object):
    def __init__(self):  # Hello World!
        self.SIZE = (1067, 600)
        self.SURF = None
        self.FPS = 30
        self.GUI_SIZE = (3200, 1800)
        self.cur_screen = None

        self.clock = pygame.time.Clock()
        pygame.font.init()
        self.fonts = {'Text Box': pygame.font.SysFont('Agency FB', 25),
                      'Title': pygame.font.SysFont('Agency FB', 20),
                      'Speech Balloon': pygame.font.SysFont('Arial', 18)}

        self.loop_thread = threading.Thread(target=self.world_loop)
        self.loop_thread.start()

        while True:  # Wait for the surface to get created
            if self.SURF is not None:
                break

    def world_loop(self):
        pygame.init()
        self.SURF = pygame.display.set_mode(self.SIZE)
        pygame.display.set_caption("Cyber!")

        while True:
            # Wait for the game to start and the screen to initialize
            if self.cur_screen is None:
                continue

            self.SURF.fill((255, 255, 255))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()
                    else:
                        self.cur_screen.check_event(event)
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.cur_screen.check_event(event)

            # Draw the current screen and its objects
            self.cur_screen.execute()
            self.cur_screen.draw_screen()
            pygame.display.update()
            self.clock.tick(self.FPS)

    def draw(self, object_surface, pos):
        self.SURF.blit(object_surface, pos)
