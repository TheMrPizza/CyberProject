""" Class for all of the objects on the map. """

import pygame
import os


class MapObject(object):
    def __init__(self, world, pos, surface=None, image=None, size=None, square=None, middle=None, is_visible=True,
                 is_clickable=True, layer=2):
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
        if not hasattr(self, 'is_visible'):
            self.is_visible = is_visible
        self.is_clickable = is_clickable
        self.layer = layer
        self.is_focus = False

    def check_collision(self, pos):
        """
        Checks if the given position is in the object.
        :param pos: Given position to check;
        :return: True if the position is in the object, otherwise False;
        """
        if self.pos[0] <= pos[0] < self.pos[0] + self.width:
            if self.pos[1] <= pos[1] < self.pos[1] + self.height:
                return True
        return False

    def draw_object(self):
        if self.is_visible:
            self.world.draw(self.surface, self.pos)

    def change_visible(self, is_visible=None):
        if is_visible is not None:
            self.is_visible = is_visible
        else:
            self.is_visible = not self.is_visible

    def change_clickable(self, is_clickable=None):
        if is_clickable is not None:
            self.is_clickable = is_clickable
        else:
            self.is_clickable = not self.is_clickable

    @staticmethod
    def merge_surfaces_horizontal(surfaces):
        """
        Merges the surfaces one by one into a surface in horizontal direction.
        :param surfaces: The surfaces to merge.
        :return: The merged surface.
        """
        merged = pygame.Surface((sum(map(lambda s: s.get_size()[0], surfaces)),
                                 surfaces[0].get_size()[1]), pygame.SRCALPHA)
        width = 0
        for i in surfaces:
            merged.blit(i, (width, 0))
            width += i.get_size()[0]
        return merged

    @staticmethod
    def find_middle(surface, parent):
        """
        Finds the left-top point of the surface position so it would be in the middle of its parent.
        :param surface: The surface to find its position.
        :param parent: The parent MapObject or pygame.Rect to find its middle.
        :return: List of x and y of the surface position.
        """
        if isinstance(parent, MapObject):
            x = parent.pos[0] + parent.width / 2 - surface.get_size()[0] / 2
            y = parent.pos[1] + parent.height / 2 - surface.get_size()[1] / 2
            return [x, y]
        elif isinstance(parent, pygame.Rect):
            x = parent.x + parent.width / 2 - surface.get_size()[0] / 2
            y = parent.y + parent.height / 2 - surface.get_size()[1] / 2
            return [x, y]

    @staticmethod
    def load_image(world, image, size=None, square=None):
        """
        Loads the given image path from the computer or the server in the given sizes.
        :param world: World object.
        :param image: Image path to load.
        :param size: List of width and height of the image. If one of them is None, it will be calculated
        proportionally.
        :param square: Width or height limit of the image.
        :return: The image surface.
        """
        if not os.path.exists(world.PATH + '/images'):
            os.makedirs(world.PATH + '/images')
        world.client.get_from_storage(image)
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
