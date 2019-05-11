from NinePatch import NinePatch
from MapObject import MapObject


class ImageButton(NinePatch):
    def __init__(self, world, pos, bg, bg_size, front=None, **kwargs):
        NinePatch.__init__(self, world, pos, bg, image_size=bg_size, layer=8)
        if front:
            self.front = MapObject(world, [None, None], image=front, middle=self, **kwargs)
        else:
            self.front = None

    def change_image(self, image, **kwargs):
        self.front = MapObject(self.world, [None, None], image=image, middle=self, **kwargs)

    def change_visible(self, is_visible=None):
        if is_visible:
            change = is_visible
        else:
            change = not self.is_visible
        self.is_visible = change
        if self.front:
            self.front.change_visible(change)

    def change_clickable(self, is_clickable=None):
        if is_clickable:
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
