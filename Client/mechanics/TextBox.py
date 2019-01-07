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
            return data
        elif self.world.fonts['Text Box'].size(self.text + event.unicode)[0] <= self.text_rect.width:
            self.text += event.unicode
        self.text_object.surface = self.world.fonts['Text Box'].render(self.text, False, (0, 0, 0))

    def on_send(self):
        self.world.cur_screen.players[0].msg = self.text  # TODO: Send message to Server

    def draw_object(self):
        self.world.draw(self.surface, self.pos)
        self.world.draw(self.text_object.surface, self.text_object.pos)
