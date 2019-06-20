import pygame
from Client.mechanics.MapObject import MapObject


class Screen(object):
    def __init__(self, world, screen_id, bg_image):
        self.world = world
        self.screen_id = screen_id
        self.bg_image = MapObject(self.world, [0, 0], image=bg_image, size=self.world.SIZE, layer=0)

    def check_event(self, event, objects=None):
        if not objects:
            objects = []
        for i in sorted(objects, key=lambda o: o.layer, reverse=True):
            if event.type == pygame.MOUSEBUTTONDOWN:
                if i.check_collision(event.pos) and i.is_clickable and \
                        i.surface.get_at([event.pos[0] - i.pos[0], event.pos[1] - i.pos[1]]).a != 0:
                    for j in objects:  # TODO: List comprehension
                        j.is_focus = False
                    i.is_focus = True
                    self.world.cur_screen.on_click(i, event)
                    break
            elif event.type == pygame.KEYDOWN:
                if i.is_focus:
                    self.world.cur_screen.on_type(i, event)

    def check_scroll(self, event, objects=None):
        if not objects:
            objects = []
        for i in objects:
            if i.check_collision(event.pos):
                self.world.cur_screen.on_scroll(i, event)
                break

    def draw_screen(self, objects=None):
        if not objects:
            objects = []
        objects = [self.bg_image] + objects
        for i in sorted(objects, key=lambda o: o.layer):
            i.draw_object()

    def execute(self):
        raise NotImplementedError

    def on_click(self, map_object, event):
        raise NotImplementedError

    def on_type(self, map_object, event):
        raise NotImplementedError

    def layer_reorder(self):
        raise NotImplementedError
