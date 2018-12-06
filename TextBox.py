from MapObject import MapObject
from NinePatch import NinePatch
import pygame


class TextBox(NinePatch):
    def __init__(self, world, pos, width, middle=None):
        NinePatch.__init__(self, world, pos, 'images/text_box.9.png', [width, 50], middle=middle, layer=4)
        self.text = ''
        self.text_surface = self.world.fonts['Text Box'].render(self.text, False, (0, 0, 0))

    def on_click(self):
        print 'Someone clicked me!'

    def on_type(self, event):
        if event.key == pygame.K_BACKSPACE:
            self.text = self.text[:-1]
        elif event.key == pygame.K_RETURN and self.text != '':
            self.on_send()
            self.text = ''
        elif self.world.fonts['Text Box'].size(self.text + event.unicode)[0] <= self.surface.get_size()[0]:
            self.text += event.unicode
        self.text_surface = self.world.fonts['Text Box'].render(self.text, False, (0, 0, 0))

    def on_send(self):
        print self.text  # TODO: Send message to server

    def draw_object(self):
        self.world.draw(self.surface, self.pos)
        # TODO: Start from text area
        self.world.draw(self.text_surface, (self.pos[0] + 20, MapObject.find_middle(self.text_surface, self)[1]))
