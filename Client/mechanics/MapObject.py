""" Class for all of the objects on the map. """

import pygame
import os


class MapObject(object):
    def __init__(self, world, pos, surface=None, image=None, size=None, square=None, middle=None, is_transparent=False, layer=2):
        self.world = world
        if not surface:
            if image:
                self.surface = MapObject.load_image(self.world, image, size, square)
            else:
                print 'No surface or image!'
        else:
            self.surface = surface

        self.pos = pos
        if None in self.pos:
            if not middle:
                print 'No pos or middle!'
            middle = MapObject.find_middle(self.surface, middle)
            if not pos[0]:
                pos[0] = middle[0]
            if not pos[1]:
                pos[1] = middle[1]

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
        if isinstance(parent, MapObject):
            x = parent.pos[0] + parent.width / 2 - surface.get_size()[0] / 2
            y = parent.pos[1] + parent.height / 2 - surface.get_size()[1] / 2
            return [x, y]
        elif isinstance(parent, pygame.Rect):
            x = parent.x + parent.width / 2 - surface.get_size()[0] / 2
            y = parent.y + parent.height / 2 - surface.get_size()[1] / 2
            return [x, y]
        else:
            print 'No!'  # TODO: Add error

    @staticmethod
    def load_image(world, image, size=None, square=None):
        if not os.path.exists(world.PATH + '/images'):
            os.makedirs(world.PATH + '/images')
        if image not in world.storage_history:
            world.client.get_from_storage(image)
            world.storage_history.append(image)
        surface = pygame.image.load(world.PATH + image)
        if image.endswith('.9.png'):  # No resize
            return surface
        if not size:
            size = [None, None]
        if square:
            if surface.get_size()[0] > surface.get_size()[1]:
                size[0] = square
                size[1] = surface.get_size()[1] * square / surface.get_size()[0]
            else:
                size[1] = square
                size[0] = surface.get_size()[0] * square / surface.get_size()[1]
        ratio = float(world.GUI_SIZE[0]) / world.SIZE[0], float(world.GUI_SIZE[1]) / world.SIZE[1]
        if not size[0]:
            size[0] = int(surface.get_size()[0] / ratio[0])
        if not size[1]:
            size[1] = int(surface.get_size()[1] / ratio[1])
        return pygame.transform.smoothscale(surface, size)
