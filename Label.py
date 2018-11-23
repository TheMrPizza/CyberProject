from MapObject import MapObject


class Label(MapObject):
    def __init__(self, world, x, y, text, font):
        self.text_surface = world.fonts[font].render(text, False, (0, 0, 0))
        MapObject.__init__(self, world, x, y, self.text_surface)
        self.text = text
        self.font = font

    def on_click(self):
        pass

    def on_type(self, event):
        pass

    def check_collision(self, pos):
        return False

    def draw_object(self):
        self.world.draw(self.text_surface, (self.x, self.y))
