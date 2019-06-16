import pygame
import sys
import threading


class World(object):
    def __init__(self, path, client):  # Hello World!
        self.SIZE = (1067, 600)
        self.SURF = None
        self.FPS = 30
        self.GUI_SIZE = (3200, 1800)
        self.PATH = path
        self.client = client
        self.cur_screen = None
        self.cur_player = None

        self.clock = pygame.time.Clock()
        pygame.font.init()
        self.fonts = {'Small': pygame.font.SysFont('coolveticacondensedrgregular', 19),
                      'Regular': pygame.font.SysFont('coolveticacondensedrgregular', 28),
                      'Medium': pygame.font.SysFont('coolveticacondensedrgregular', 31),
                      'Large': pygame.font.SysFont('coolveticacondensedrgregular', 72),
                      'Big': pygame.font.SysFont('coolveticacondensedrgregular', 100),
                      'Title': pygame.font.SysFont('coolveticacondensedrgregular', 60),
                      'Speech Balloon': pygame.font.SysFont('coolveticacondensedrgregular', 34),
                      'Compressed': pygame.font.SysFont('coolveticacompressedrgregular', 40),
                      'Username': pygame.font.SysFont('coolveticacondensedrgregular', 24),
                      'NPC': pygame.font.SysFont('coolveticacondensedrgregular', 28)}

        self.loop_thread = threading.Thread(target=self.world_loop)
        self.loop_thread.start()

        while True:  # Wait for the surface to get created
            if self.SURF is not None:
                break

    def world_loop(self):
        pygame.init()
        self.SURF = pygame.display.set_mode(self.SIZE)
        from MapObject import MapObject
        icon = MapObject.load_image(self, 'images/elements/icon.png')
        pygame.display.set_icon(icon)
        pygame.display.set_caption('Volantis')
        execute_thread = threading.Thread(target=self.execute_loop)
        execute_thread.start()

        while True:
            # Wait for the game to start and the screen to initialize
            if self.cur_screen is None:
                continue

            self.SURF.fill((255, 255, 255))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.client.quit(self.cur_player.username, self.cur_player.room_id)
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.client.quit(self.cur_player.username, self.cur_player.room_id)
                        pygame.quit()
                        sys.exit()
                    else:
                        self.cur_screen.check_event(event)
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button in [4, 5]:
                        self.cur_screen.check_scroll(event)
                    else:
                        self.cur_screen.check_event(event)

            # Draw the current screen and its objects
            self.cur_screen.draw_screen()
            pygame.display.update()
            self.clock.tick(self.FPS)

    def execute_loop(self):
        while True:
            if self.cur_screen is None:
                continue
            self.cur_screen.execute()

    def draw(self, object_surface, pos, **kwargs):
        self.SURF.blit(object_surface, pos, **kwargs)
