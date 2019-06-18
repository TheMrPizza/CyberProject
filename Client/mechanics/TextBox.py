from Resources import colors, fonts
from MapObject import MapObject
from NinePatch import NinePatch
import pygame


class TextBox(NinePatch):
    def __init__(self, world, pos, width, is_enter=True, color=colors['black'], **kwargs):
        NinePatch.__init__(self, world, pos, 'images/elements/light_blue_cell.9.png', [width, 45], **kwargs)
        self.text = ''
        self.width = width
        self.color = color
        self.is_enter = is_enter
        self.text_object = MapObject(world, [self.text_rect.x, None],
                                     fonts['Regular'].render(self.text, True, self.color),
                                     layer=5, middle=self.text_rect)

    def change_background(self, image, **kwargs):
        NinePatch.__init__(self, self.world, self.pos, image, [self.width, 45], **kwargs)

    def on_type(self, event):
        if event.key == pygame.K_BACKSPACE:
            self.text = self.text[:-1]
        elif event.key == pygame.K_RETURN and self.text != '':
            if not self.is_enter:
                return
            data = self.text
            self.text = ''
            self.text_object.surface = fonts['Regular'].render(self.text, True, self.color)
            return data
        elif len(event.unicode) != 1 or ord(event.unicode) < 32 or ord(event.unicode) > 126:
            return
        elif fonts['Regular'].size(self.text + event.unicode)[0] <= self.text_rect.width:
            self.text += event.unicode
        self.text_object.surface = fonts['Regular'].render(self.text, True, self.color)

    def on_send(self, data):
        self.world.cur_player.msg = data
        self.world.client.chat(self.world.cur_player.username, data)

    def draw_object(self):
        self.world.draw(self.surface, self.pos)
        self.world.draw(self.text_object.surface, self.text_object.pos)
