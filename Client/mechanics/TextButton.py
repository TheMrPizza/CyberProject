from NinePatch import NinePatch
from MapObject import MapObject


class TextButton(NinePatch):
    def __init__(self, world, pos, bg, bg_size, text=None, font=None, color=(0, 0, 0), **kwargs):
        middle, layer = None, 10
        if 'middle' in kwargs:
            middle = kwargs['middle']
            kwargs.pop('middle')
        if 'layer' in kwargs:
            layer = kwargs['layer']
        NinePatch.__init__(self, world, pos, bg, image_size=bg_size, middle=middle, layer=layer)
        if text and font:
            self.front = MapObject(world, [None, None], self.world.fonts[font].render(text, True, color), middle=self.text_rect, **kwargs)
        else:
            self.front = None

    def change_bg(self, image, image_size):
        NinePatch.__init__(self, self.world, self.pos, image, image_size=image_size, layer=8)

    def change_front(self, text, font, color=(0, 0, 0), **kwargs):
        self.front = MapObject(self.world, [None, None], self.world.fonts[font].render(text, True, color), layer=5,
                               middle=self.text_rect, **kwargs)

    def update_pos(self, pos):
        if self.front:
            self.front.pos[0] += pos[0] - self.pos[0]
            self.front.pos[1] += pos[1] - self.pos[1]
        self.pos = pos

    def change_visible(self, is_visible=None):
        if is_visible is not None:
            change = is_visible
        else:
            change = not self.is_visible
        self.is_visible = change
        if self.front:
            self.front.change_visible(change)

    def change_clickable(self, is_clickable=None):
        if is_clickable is not None:
            change = is_clickable
        else:
            change = not self.is_clickable
        self.is_clickable = change
        if self.front:
            self.front.change_clickable(change)

    def draw_object(self):
        NinePatch.draw_object(self)
        if self.front:
            self.front.draw_object()

    def draw_item(self, surface):
        surface.blit(self.surface, self.pos)
        if self.front:
            surface.blit(self.front.surface, self.front.pos)
