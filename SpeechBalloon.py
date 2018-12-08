from NinePatch import NinePatch
from MapObject import MapObject


class SpeechBalloon(NinePatch):
    def __init__(self, world, pos, text, **kwargs):
        self.MAX_WIDTH = 200
        self.FONT = world.fonts['Speech Balloon']
        self.text = SpeechBalloon.size_adjustment(text, self.FONT, self.MAX_WIDTH)
        NinePatch.__init__(self, world, pos, 'images/test_balloon.9.png', [200, 100], layer=4, **kwargs)
        self.lines = SpeechBalloon.create_lines(world, self.pos, self.text, self.FONT, self.text_rect)

    @staticmethod
    def size_adjustment(text, font, max_width):
        words = text.split(' ')
        text = ''
        last = 0
        for i in xrange(len(words)):
            if font.size(' '.join(words[last:i+1]))[0] > max_width:
                text += ' '.join(words[last:i]) + '\n'
                last = i
            elif i == len(words)-1:
                text += ' '.join(words[last:i+1]) + '\n'
                last = i
        return text[:-1]

    @staticmethod
    def create_lines(world, pos, text, font, text_rect):
        lines = text.split('\n')
        height = font.size(text)[1]
        for i in xrange(len(lines)):
            lines[i] = MapObject(world, [None, pos[1] + height * i], font.render(lines[i], False, (0, 0, 0)), middle=text_rect, layer=5)
        return lines

    def update(self, pos, text):
        self.text_rect.x += pos[0] - self.pos[0]
        self.text_rect.y += pos[1] - self.pos[1]
        self.pos = pos
        self.text = SpeechBalloon.size_adjustment(text, self.FONT, self.MAX_WIDTH)
        self.lines = SpeechBalloon.create_lines(self.world, self.pos, self.text, self.FONT, self.text_rect)

    def draw_object(self):
        self.world.draw(self.surface, self.pos)
        for i in self.lines:
            self.world.draw(i.surface, i.pos)
