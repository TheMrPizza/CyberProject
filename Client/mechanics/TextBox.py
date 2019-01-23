from MapObject import MapObject
from NinePatch import NinePatch
import pygame


class TextBox(NinePatch):
    def __init__(self, world, pos, width, middle=None):
        NinePatch.__init__(self, world, pos, 'images/test_text_box.9.png', [width, 50], middle=middle, layer=4)
        self.text = ''
        self.text_object = MapObject(world, (self.text_rect.x, self.text_rect.y), self.world.fonts['Text Box'].render(self.text, False, (0, 0, 0)), layer=5)

    def on_click(self):
        print 'Someone clicked me!'

    def on_type(self, event):
        if event.key == pygame.K_BACKSPACE:
            self.text = self.text[:-1]
        elif event.key == pygame.K_RETURN and self.text != '':
            data = self.text
            self.text = ''
            self.text_object.surface = self.world.fonts['Text Box'].render(self.text, False, (0, 0, 0))
            return data
        elif self.world.fonts['Text Box'].size(self.text + event.unicode)[0] <= self.text_rect.width:
            self.text += event.unicode
        self.text_object.surface = self.world.fonts['Text Box'].render(self.text, False, (0, 0, 0))

    def on_send(self, data):
        self.world.cur_player.msg = data
        self.world.client.chat(self.world.cur_player.username, data)

    def draw_object(self):
        self.world.draw(self.surface, self.pos)
        self.world.draw(self.text_object.surface, self.text_object.pos)
