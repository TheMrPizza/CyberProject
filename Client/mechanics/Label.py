from MapObject import MapObject


class Label(MapObject):
    def __init__(self, world, pos, text, font, color=(0, 0, 0), **kwargs):
        self.text_surface = world.fonts[font].render(text, True, color)
        MapObject.__init__(self, world, pos, self.text_surface, **kwargs)
        self.text = text
        self.font = font

    def draw_object(self):
        self.world.draw(self.text_surface, self.pos)
