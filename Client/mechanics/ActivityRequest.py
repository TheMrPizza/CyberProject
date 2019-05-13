from NinePatch import NinePatch
from ImageButton import ImageButton


class ActivityRequest(NinePatch):
    def __init__(self, world, activity, player, is_incoming):
        NinePatch.__init__(self, world, [20, 20], 'images/test_text_box.9.png', [150, 60], layer=8)
        self.activity = activity
        self.player = player
        self.is_incoming = is_incoming
        self.buttons = {}
        if self.is_incoming:
            self.buttons['v'] = ImageButton(world, [140, 30], 'images/green_cell.9.png', [20, 20], front='images/v.png', square=15)
            self.buttons['x'] = ImageButton(world, [140, 50], 'images/red_cell.9.png', [20, 20], front='images/x.png', square=15)
        else:
            self.buttons['x'] = ImageButton(world, [140, 40], 'images/red_cell.9.png', [20, 20], front='images/x.png', square=15)

    def change_visible(self, is_visible=None):
        if is_visible:
            change = is_visible
        else:
            change = not self.is_visible
        self.is_visible = change
        for i in self.buttons:
            i.change_visible(change)

    def change_clickable(self, is_clickable=None):
        if is_clickable:
            change = is_clickable
        else:
            change = not self.is_clickable
        self.is_clickable = change
        for i in self.buttons:
            i.change_clickable(change)

    def draw_object(self):
        if self.is_visible:
            NinePatch.draw_object(self)
            self.world.draw(self.player.text_object.surface, [60, 40])
            for i in self.buttons:
                self.buttons[i].draw_object()
