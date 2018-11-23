import pygame


class Screen:
    def __init__(self, world, screen_id, image):
        self.world = world
        self.screen_id = screen_id
        self.image = image
        self.buttons = []

    def check_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            for i in self.buttons:
                if i.check_collision(event.pos):
                    i.is_focus = True
                    i.on_click()
                else:
                    i.is_focus = False
        elif event.type == pygame.KEYDOWN:
            for i in self.buttons:
                if i.is_focus:
                    i.on_type(event)

    def draw_screen(self):
        # self.world.draw(self.image, (0, 0)) TODO: Add image to Login
        for i in self.buttons:
            i.draw_object()
