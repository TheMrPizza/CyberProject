from NinePatch import NinePatch
from MapObject import MapObject


class ImageButton(NinePatch):
    def __init__(self, world, pos, bg, bg_size, front=None, **kwargs):
        NinePatch.__init__(self, world, pos, bg, image_size=bg_size, layer=8)
        if front:
            self.front = MapObject(world, [None, None], image=front, middle=self, **kwargs)
        else:
            self.front = None

    def draw_object(self):
        NinePatch.draw_object(self)
        if self.front:
            self.front.draw_object()
