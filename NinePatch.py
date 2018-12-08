""" Class for stretchable and resizable images (buttons, text boxes and more).
In order to save the image's quality, it's divided into 9 parts so the whole image's
size can change correctly.

For more information about NinePatch: https://developer.android.com/guide/topics/graphics/drawables#nine-patch
About the 9-Slice Scaling technique: https://en.wikipedia.org/wiki/9-slice_scaling """

import pygame
from MapObject import MapObject


class NinePatch(MapObject):
    def __init__(self, world, pos, image, size, **kwargs):
        self.surface, self.text_rect = NinePatch.create(pygame.image.load(image), size)
        MapObject.__init__(self, world, pos, surface=self.surface, **kwargs)
        self.text_rect.x += self.pos[0]
        self.text_rect.y += self.pos[1]

    @staticmethod
    def create(image, size):
        x, y, text_x, text_y = NinePatch.find_borders(image)

        # Cut the borders (4 pixels wide)
        cur_image = pygame.Surface((image.get_size()[0]-4, image.get_size()[1]-4), pygame.SRCALPHA)
        cur_image.blit(image, (0, 0), area=(2, 2, image.get_size()[0]-2, image.get_size()[1]-2))

        # Stretch the width so the width/height ratio will be as requested
        surfaces = []
        ratio = float(size[0]) / size[1]

        # Y-Top
        left = pygame.Surface((x['start'], y['start']), pygame.SRCALPHA)
        left.blit(cur_image, (0, 0), area=(0, 0, x['start'], y['start']))

        middle = pygame.Surface((x['end'] - x['start'], y['start']), pygame.SRCALPHA)
        middle.blit(cur_image, (0, 0), area=(x['start'], 0, x['end'] - x['start'], y['start']))
        # TODO: Raise exception for proportion ratio
        try:
            middle = pygame.transform.smoothscale(middle, (int(cur_image.get_size()[1] * ratio) - x['start'] -
                                                     (cur_image.get_size()[0] - x['end']), y['start']))
        except ValueError, pygame.error:
            raise SizeError('The width, height or their ratio is too big.')

        right = pygame.Surface((cur_image.get_size()[0] - x['end'], y['start']), pygame.SRCALPHA)
        right.blit(cur_image, (0, 0), area=(x['end'], 0, cur_image.get_size()[0] - x['end'], y['start']))

        surfaces.append([left, middle, right])

        # Y-Middle
        left = pygame.Surface((x['start'], y['end'] - y['start']), pygame.SRCALPHA)
        left.blit(cur_image, (0, 0), area=(0, y['start'], x['start'], y['end'] - y['start']))

        middle = pygame.Surface((x['end'] - x['start'], y['end'] - y['start']), pygame.SRCALPHA)
        middle.blit(cur_image, (0, 0), area=(x['start'], y['start'], x['end'] - x['start'], y['end'] - y['start']))
        middle = pygame.transform.smoothscale(middle, (int(cur_image.get_size()[1] * ratio) - x['start'] -
                                                 (cur_image.get_size()[0] - x['end']), y['end'] - y['start']))

        right = pygame.Surface((cur_image.get_size()[0] - x['end'], y['end'] - y['start']), pygame.SRCALPHA)
        right.blit(cur_image, (0, 0), area=(x['end'], y['start'], cur_image.get_size()[0] - x['end'],
                                            y['end'] - y['start']))

        surfaces.append([left, middle, right])

        # Y-Bottom
        left = pygame.Surface((x['start'], cur_image.get_size()[1] - y['end']), pygame.SRCALPHA)
        left.blit(cur_image, (0, 0), area=(0, y['end'], x['start'], cur_image.get_size()[1] - y['end']))

        middle = pygame.Surface((x['end'] - x['start'], cur_image.get_size()[1] - y['end']), pygame.SRCALPHA)
        middle.blit(cur_image, (0, 0), area=(x['start'], y['end'], x['end'] - x['start'],
                                             cur_image.get_size()[1] - y['end']))
        middle = pygame.transform.smoothscale(middle, (int(cur_image.get_size()[1] * ratio) - x['start'] -
                                                 (cur_image.get_size()[0] - x['end']),
                                                 cur_image.get_size()[1] - y['end']))

        right = pygame.Surface((cur_image.get_size()[0] - x['end'], cur_image.get_size()[1] - y['end']),
                               pygame.SRCALPHA)
        right.blit(cur_image, (0, 0), area=(x['end'], y['end'], cur_image.get_size()[0] - x['end'],
                                            cur_image.get_size()[1] - y['end']))

        # Merge all the parts and resize them to the requested size
        surfaces.append([left, middle, right])
        merged = NinePatch.merge(surfaces)
        text_ratio = [float(size[0]) / merged.get_size()[0], float(size[1]) / merged.get_size()[1]]
        merged = pygame.transform.smoothscale(merged, size)

        # Stretch the width of the text area and resize it
        for i in text_x:
            if text_x[i] > x['start']:
                if text_x[i] > x['end']:  # Full stretch
                    text_x[i] += middle.get_size()[0] - (x['end'] - x['start'])
                else:  # Partial stretch
                    text_x[i] = x['start'] + int((float(text_x[i]) - x['start']) / (x['end'] - x['start']) * (middle.get_size()[0]))
            text_x[i] = int(text_x[i] * text_ratio[0])

        # Resize the height of the text area
        for i in text_y:
            text_y[i] = int(text_y[i] * text_ratio[1])
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
            print 'Format is not Nine-Patch!'
            return None

        y = {'start': None, 'end': None}  # Left line
        for i in xrange(image.get_size()[1]):
            if image.get_at((0, i)) == (0, 0, 0):
                if not y['start']:
                    y['start'] = i - 2
                y['end'] = i - 2
        if not y['start']:
            print 'Format is not Nine-Patch!'
            return None

        text_x = {'start': None, 'end': None}  # Bottom line
        for i in xrange(image.get_size()[0]):
            if image.get_at((i, image.get_size()[1] - 1)) == (0, 0, 0):
                if not text_x['start']:
                    text_x['start'] = i - 2
                text_x['end'] = i - 2
        if not text_x['start']:
            print 'Format is not Nine-Patch!'
            return None

        text_y = {'start': None, 'end': None}  # Right line
        for i in xrange(image.get_size()[1]):
            if image.get_at((image.get_size()[0] - 1, i)) == (0, 0, 0):
                if not text_y['start']:
                    text_y['start'] = i - 2
                text_y['end'] = i - 2
        if not text_y['start']:
            print 'Format is not Nine-Patch!'
            return None

        return x, y, text_x, text_y


class SizeError(Exception):
    pass
