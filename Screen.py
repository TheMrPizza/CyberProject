import pygame
from MapObject import MapObject


class Screen:
    def __init__(self, world, screen_id, bg_image):
        self.world = world
        self.screen_id = screen_id
        self.bg_image = MapObject(self.world, [0, 0], image=bg_image, size=self.world.SIZE, layer=0)

    def check_event(self, event, objects):
        for i in objects:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if i.check_collision(event.pos):
                    i.is_focus = True
                    self.world.cur_screen.on_click(i, event)
                else:
                    i.is_focus = False
            elif event.type == pygame.KEYDOWN:
                if i.is_focus:
                    self.world.cur_screen.on_type(i, event)

    def draw_screen(self, objects=None):
        if not objects:
            objects = []
        # TODO: Add image to Login
        objects = [self.bg_image] + objects
        for i in sorted(objects, key=lambda o: o.layer):
            i.draw_object()

    def execute(self):
        raise NotImplementedError

    def on_click(self, map_object, event):
        raise NotImplementedError

    def on_type(self, map_object, event):
        raise NotImplementedError
