""" Class for stretchable and resizable images (buttons, text boxes and more).
In order to save the image's quality, it's divided into 9 parts so the whole image's
size can change correctly.

For more information about NinePatch: https://developer.android.com/guide/topics/graphics/drawables#nine-patch
About the 9-Slice Scaling technique: https://en.wikipedia.org/wiki/9-slice_scaling """

import pygame
from MapObject import MapObject


class NinePatch(MapObject):
    def __init__(self, world, pos, image, image_size=None, text_size=None, **kwargs):
        if not image_size:
            if text_size:
                image_size = NinePatch.calc_image_size(world, image, text_size)
            else:
                raise SizeError('No image_size or text_size found!')
        self.surface, self.text_rect = NinePatch.create(MapObject.load_image(world, image), image_size)

        MapObject.__init__(self, world, pos, surface=self.surface, **kwargs)
        self.text_rect.x += self.pos[0]
        self.text_rect.y += self.pos[1]

    @staticmethod
    def calc_image_size(world, image, text_size):
        image = MapObject.load_image(world, image)
        x, y, text_x, text_y = NinePatch.find_borders(image)

        cur_image = pygame.Surface((image.get_size()[0] - 4, image.get_size()[1] - 4), pygame.SRCALPHA)
        cur_image.blit(image, (0, 0), area=(2, 2, image.get_size()[0] - 2, image.get_size()[1] - 2))

        return [text_x['start'] + text_size[0] + (cur_image.get_size()[0] - text_x['end']),
                text_y['start'] + text_size[1] + (cur_image.get_size()[1] - text_y['end'])]

    @staticmethod
    def create(image, size):
        x, y, text_x, text_y = NinePatch.find_borders(image)
        surfaces = []

        # Cut the borders (4 pixels wide)
        cur_image = pygame.Surface((image.get_size()[0] - 4, image.get_size()[1] - 4), pygame.SRCALPHA)
        cur_image.blit(image, (0, 0), area=(2, 2, image.get_size()[0] - 2, image.get_size()[1] - 2))

        min_width = x['start'] + (cur_image.get_size()[0] - x['end'])
        min_height = y['start'] + (cur_image.get_size()[1] - y['end'])
        if size[0] < min_width:
            size[0] = min_width
        if size[1] < min_height:
            size[1] = min_height

        # Y-Top
        left = pygame.Surface((x['start'], y['start']), pygame.SRCALPHA)
        left.blit(cur_image, (0, 0), area=(0, 0, x['start'], y['start']))

        middle = pygame.Surface((x['end'] - x['start'], y['start']), pygame.SRCALPHA)
        middle.blit(cur_image, (0, 0), area=(x['start'], 0, x['end'] - x['start'], y['start']))
        try:
            middle = pygame.transform.smoothscale(middle, (size[0] - x['start'] - (cur_image.get_size()[0] - x['end']),
                                                           y['start']))
        except ValueError, pygame.error:
            print size, x, cur_image.get_size()[0]
            raise SizeError('The width, height or their ratio is too big.')

        right = pygame.Surface((cur_image.get_size()[0] - x['end'], y['start']), pygame.SRCALPHA)
        right.blit(cur_image, (0, 0), area=(x['end'], 0, cur_image.get_size()[0] - x['end'], y['start']))

        surfaces.append([left, middle, right])

        # Y-Middle
        left = pygame.Surface((x['start'], y['end'] - y['start']), pygame.SRCALPHA)
        left.blit(cur_image, (0, 0), area=(0, y['start'], x['start'], y['end'] - y['start']))
        left = pygame.transform.smoothscale(left, (x['start'], size[1] - y['start'] -
                                                   (cur_image.get_size()[1] - y['end'])))

        middle = pygame.Surface((x['end'] - x['start'], y['end'] - y['start']), pygame.SRCALPHA)
        middle.blit(cur_image, (0, 0), area=(x['start'], y['start'], x['end'] - x['start'], y['end'] - y['start']))
        middle = pygame.transform.smoothscale(middle, (size[0] - x['start'] - (cur_image.get_size()[0] - x['end']),
                                                       size[1] - y['start'] - (cur_image.get_size()[1] - y['end'])))

        right = pygame.Surface((cur_image.get_size()[0] - x['end'], y['end'] - y['start']), pygame.SRCALPHA)
        right.blit(cur_image, (0, 0), area=(x['end'], y['start'], cur_image.get_size()[0] - x['end'],
                                            y['end'] - y['start']))
        right = pygame.transform.smoothscale(right, (cur_image.get_size()[0] - x['end'], size[1] - y['start'] -
                                                     (cur_image.get_size()[1] - y['end'])))

        surfaces.append([left, middle, right])

        # Y-Bottom
        left = pygame.Surface((x['start'], cur_image.get_size()[1] - y['end']), pygame.SRCALPHA)
        left.blit(cur_image, (0, 0), area=(0, y['end'], x['start'], cur_image.get_size()[1] - y['end']))

        middle = pygame.Surface((x['end'] - x['start'], cur_image.get_size()[1] - y['end']), pygame.SRCALPHA)
        middle.blit(cur_image, (0, 0), area=(x['start'], y['end'], x['end'] - x['start'],
                                             cur_image.get_size()[1] - y['end']))
        middle = pygame.transform.smoothscale(middle, (size[0] - x['start'] - (cur_image.get_size()[0] - x['end']),
                                                       cur_image.get_size()[1] - y['end']))

        right = pygame.Surface((cur_image.get_size()[0] - x['end'], cur_image.get_size()[1] - y['end']),
                               pygame.SRCALPHA)
        right.blit(cur_image, (0, 0), area=(x['end'], y['end'], cur_image.get_size()[0] - x['end'],
                                            cur_image.get_size()[1] - y['end']))

        surfaces.append([left, middle, right])

        # Merge all the parts
        merged = NinePatch.merge(surfaces)

        # Adjust the text area
        text_x['end'] = size[0] - (cur_image.get_size()[0] - text_x['end'])
        text_y['end'] = size[1] - (cur_image.get_size()[1] - text_y['end'])
        text_rect = pygame.Rect((text_x['start'], text_y['start']),
                                (text_x['end'] - text_x['start'], text_y['end'] - text_y['start']))
        return merged, text_rect

    @staticmethod
    def merge(surfaces):
        width = sum(map(lambda s: s.get_size()[0], surfaces[0]))
        height = sum(map(lambda s: s.get_size()[1], zip(*surfaces)[0]))

        merged = pygame.Surface((width, height), pygame.SRCALPHA)
        width, height = 0, 0
        for i in surfaces:
            for j in i:
                merged.blit(j, (width, height))
                width += j.get_size()[0]
            width = 0
            height += i[0].get_size()[1]
        return merged

    @staticmethod
    def find_borders(image):
        # Find black lines at the borders
        x = {'start': None, 'end': None}  # Top line
        for i in xrange(image.get_size()[0]):
            if image.get_at((i, 0)) == (0, 0, 0):
                if not x['start']:
                    x['start'] = i - 2
                x['end'] = i - 2
        if not x['start']:
            raise FormatError('Format is not Nine-Patch!\nPlease follow the instructions here: '
                              'https://developer.android.com/guide/topics/graphics/drawables#nine-patch')

        y = {'start': None, 'end': None}  # Left line
        for i in xrange(image.get_size()[1]):
            if image.get_at((0, i)) == (0, 0, 0):
                if not y['start']:
                    y['start'] = i - 2
                y['end'] = i - 2
        if not y['start']:
            raise FormatError('Format is not Nine-Patch!\nPlease follow the instructions here: '
                              'https://developer.android.com/guide/topics/graphics/drawables#nine-patch')

        text_x = {'start': None, 'end': None}  # Bottom line
        for i in xrange(image.get_size()[0]):
            if image.get_at((i, image.get_size()[1] - 1)) == (0, 0, 0):
                if not text_x['start']:
                    text_x['start'] = i - 2
                text_x['end'] = i - 2
        if not text_x['start']:
            raise FormatError('Format is not Nine-Patch!\nPlease follow the instructions here: '
                              'https://developer.android.com/guide/topics/graphics/drawables#nine-patch')

        text_y = {'start': None, 'end': None}  # Right line
        for i in xrange(image.get_size()[1]):
            if image.get_at((image.get_size()[0] - 1, i)) == (0, 0, 0):
                if not text_y['start']:
                    text_y['start'] = i - 2
                text_y['end'] = i - 2
        if not text_y['start']:
            raise FormatError('Format is not Nine-Patch!\nPlease follow the instructions here: '
                              'https://developer.android.com/guide/topics/graphics/drawables#nine-patch')

        return x, y, text_x, text_y

# Nine-Patch Exceptions


class FormatError(Exception):
    pass


class SizeError(Exception):
    pass
