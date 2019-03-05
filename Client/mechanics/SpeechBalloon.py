import pygame
from NinePatch import NinePatch
from MapObject import MapObject


class SpeechBalloon(NinePatch):
    def __init__(self, world, pos, text, **kwargs):
        self.MAX_WIDTH = 100  # px
        self.FONT = world.fonts['Speech Balloon']
        self.TTL = 5000  # ms
        self.is_alive = True

        text = SpeechBalloon.size_adjustment(text, self.FONT, self.MAX_WIDTH)
        pos = [pos[0] + 40, pos[1] - 60]
        NinePatch.__init__(self, world, pos, 'images/test_speech_balloon.9.png',
                           text_size=SpeechBalloon.calc_text_size(text, self.FONT), layer=4, **kwargs)
        self.lines = SpeechBalloon.create_lines(world, [self.text_rect.x, self.text_rect.y], text, self.FONT,
                                                self.text_rect)

        self.start_time = pygame.time.get_ticks()

    @staticmethod
    def size_adjustment(text, font, max_width):
        words = text.split(' ')
        text = []
        last = 0
        for i in xrange(len(words)):
            if font.size(' '.join(words[last:i+1]))[0] > max_width and last != i:
                text.append(' '.join(words[last:i]))
                last = i
            if i == len(words)-1:
                text.append(' '.join(words[last:i+1]))
                last = i
        return text

    @staticmethod
    def create_lines(world, pos, lines, font, text_rect):
        height = font.size(lines[0])[1]
        for i in xrange(len(lines)):
            lines[i] = MapObject(world, [None, pos[1] + height * i], font.render(lines[i], False, (0, 0, 0)),
                                 middle=text_rect, layer=5)
        return lines

    @staticmethod
    def calc_text_size(lines, font):
        max_width = 0
        height = 0
        for i in lines:
            line_size = font.size(i)
            if line_size[0] > max_width:
                max_width = line_size[0]
            height += line_size[1]
        return [max_width, height]

    def update(self, pos):
        pos = [pos[0] + 40, pos[1] - 60]
        for i in self.lines:
            i.pos[0] += pos[0] - self.pos[0]
            i.pos[1] += pos[1] - self.pos[1]
        self.text_rect.x += pos[0] - self.pos[0]
        self.text_rect.y += pos[1] - self.pos[1]
        self.pos = pos

    def draw_object(self):
        if pygame.time.get_ticks() - self.start_time >= self.TTL:
            self.is_alive = False
            return
        self.world.draw(self.surface, self.pos)
        for i in self.lines:
            self.world.draw(i.surface, i.pos)
