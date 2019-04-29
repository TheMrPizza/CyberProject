from NinePatch import NinePatch
from ImageButton import ImageButton


class TradeRequest(NinePatch):
    def __init__(self, world, player, is_incoming):
        NinePatch.__init__(self, world, [20, 20], 'images/test_text_box.9.png', [100, 25], layer=8)
        self.player = player
        self.is_incoming = is_incoming
        self.buttons = {}
        if self.is_incoming:
            self.buttons['v'] = ImageButton(world, [80, 21], 'images/green_cell.9.png', [10, 10], front='images/v.png', square=8)
            self.buttons['x'] = ImageButton(world, [80, 34], 'images/green_cell.9.png', [10, 10], front='images/x.png', square=8)
        else:
            self.buttons['x'] = ImageButton(world, [80, 27], 'images/green_cell.9.png', [10, 10], front='images/x.png', square=8)

    def draw_object(self):
        NinePatch.draw_object(self)
        self.world.draw(self.player.text_object.surface, [40, 27])
        for i in self.buttons:
            self.buttons[i].draw_object()
