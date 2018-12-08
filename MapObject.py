""" Class for all of the objects on the map. """

import pygame


class MapObject(object):
    def __init__(self, world, pos, surface=None, image=None, size=None, middle=None, is_transparent=False, layer=2):
        self.world = world
        if surface is None:
            if image is not None:
                self.surface = MapObject.load_image(self.world, image, size)
            else:
                print 'No surface or image!'
        else:
            self.surface = surface

        self.pos = pos
        if None in self.pos:
            if middle is None:
                print 'No pos or middle!'
            middle = MapObject.find_middle(self.surface, middle)
            if pos[0] is None:
                if pos[1] is None:
                    self.pos = middle
                else:
                    self.pos[0] = middle[0]
            else:
                self.pos[1] = middle[1]

        self.width = self.surface.get_size()[0]
        self.height = self.surface.get_size()[1]
        self.is_transparent = is_transparent
        self.layer = layer
        self.is_focus = False

    def check_collision(self, pos):
        if self.pos[0] <= pos[0] < self.pos[0] + self.width:
            if self.pos[1] <= pos[1] < self.pos[1] + self.height:
                return True
        return False

    def draw_object(self):
        if not self.is_transparent:
            self.world.draw(self.surface, self.pos)

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
    def find_middle(surface, parent):
        if type(parent) is MapObject:
            x = parent.pos[0] + parent.width / 2 - surface.get_size()[0] / 2
            y = parent.pos[1] + parent.height / 2 - surface.get_size()[1] / 2
            return [x, y]
        elif type(parent) is pygame.Rect:
            x = parent.x + parent.width / 2 - surface.get_size()[0] / 2
            y = parent.y + parent.height / 2 - surface.get_size()[1] / 2
            return [x, y]
        else:
            print 'No!'

    @staticmethod
    def load_image(world, image, size=None):
        if size is None:
            size = [None, None]
        surface = pygame.image.load(image)
        ratio = float(world.GUI_SIZE[0]) / world.SIZE[0], float(world.GUI_SIZE[1]) / world.SIZE[1]
        if size[0] is None:
            size[0] = int(surface.get_size()[0] / ratio[0])
        if size[1] is None:
            size[1] = int(surface.get_size()[1] / ratio[1])
        return pygame.transform.smoothscale(surface, size)
