from ImageButton import ImageButton
from MapObject import MapObject


class MapMenu(ImageButton):
    def __init__(self, world, room_id):
        ImageButton.__init__(self, world, [None, -10], 'images/elements/light_blue_cell.9.png', [949, 544], image='images/elements/map.png', middle=world.cur_screen.bg_image, layer=8)
        self.buttons = [MapObject(self.world, [630, 387], image='images/elements/beach_button.png', layer=9),
                        MapObject(self.world, [760, 440], image='images/elements/submarine_button.png', layer=9),
                        MapObject(self.world, [307, 260], image='images/elements/forest_button.png', layer=9),
                        MapObject(self.world, [338, 117], image='images/elements/plaza_button.png', layer=9),
                        MapObject(self.world, [415, 192], image='images/elements/market_button.png', layer=9),
                        MapObject(self.world, [775, 67], image='images/elements/mountain_button.png', layer=9)]
        self.x_button = ImageButton(self.world, [68, 5], 'images/elements/light_red_color.9.png', [30, 30], image='images/elements/white_x.png', square=18)
        self.room_id = room_id
        self.change_visible(False)
        self.change_clickable(False)

    def change_visible(self, is_visible=None):
        if is_visible is not None:
            change = is_visible
        else:
            change = not self.is_visible
        self.is_visible = change
        for i in self.buttons:
            i.is_visible = change
        self.x_button.is_visible = change

    def change_clickable(self, is_clickable=None):
        if is_clickable is not None:
            change = is_clickable
        else:
            change = not self.is_clickable
        self.is_clickable = change
        for i in self.buttons:
            i.is_clickable = change
        self.buttons[self.room_id - 201].change_clickable(False)  # Same room
        self.x_button.is_clickable = change

    def draw_object(self):
        if self.is_visible:
            ImageButton.draw_object(self)
            for i in self.buttons:
                i.draw_object()
            self.x_button.draw_object()
