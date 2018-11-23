""" Class for all of the objects on the map.
Inherited classes should override some of the functions,
otherwise NotImplementedError will be raised."""
import pygame


class MapObject:
    def __init__(self, world, x, y, surface):
        self.world = world
        self.x = x
        self.y = y
        self.surface = surface
        self.width = self.surface.get_size()[0]
        self.height = self.surface.get_size()[1]
        self.is_focus = False

    @staticmethod
    def merge_surfaces_horizontal(surfaces):
        merged = pygame.Surface((sum(map(lambda s: s.get_size()[0], surfaces)),
                                 surfaces[0].get_size()[1]), pygame.SRCALPHA)
        width = 0
        for i in surfaces:
            merged.blit(i, (width, 0))
            width += i.get_size()[0]
        return merged

    @staticmethod
    def find_middle(map_object, surface, is_x, is_y):
        x = map_object.x + map_object.width / 2 - surface.get_size()[0] / 2
        y = map_object.y + map_object.height / 2 - surface.get_size()[1] / 2
        if is_x and is_y:
            return x, y
        if is_x:
            return x
        if is_y:
            return y

    def check_collision(self, pos):
        if self.x <= pos[0] < self.x + self.width:
            if self.y <= pos[1] < self.y + self.height:
                return True
        return False

    def on_click(self):
        raise NotImplementedError

    def on_type(self, event):
        raise NotImplementedError

    def draw_object(self):
        raise NotImplementedError
