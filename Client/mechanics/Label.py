from MapObject import MapObject


class Label(MapObject):
    def __init__(self, world, pos, text, font, color=(0, 0, 0)):
        self.text_surface = world.fonts[font].render(text, False, color)
        MapObject.__init__(self, world, pos, self.text_surface)
        self.text = text
        self.font = font

    def check_collision(self, pos):
        return False

    def draw_object(self):
        self.world.draw(self.text_surface, self.pos)
