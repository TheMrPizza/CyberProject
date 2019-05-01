from MapObject import MapObject
from ImageButton import ImageButton
from NinePatch import NinePatch
from Label import Label


class PlayerInfoMenu(NinePatch):
    def __init__(self, world):
        NinePatch.__init__(self, world, [400, -10], 'images/test_text_box.9.png', [300, 340], layer=8)
        self.player = None
        self.stage = MapObject(world, [430, -10], image='images/stage.png')
        self.arrow = MapObject(world, [460, 280], image='images/green_arrow.png')
        self.level = Label(world, [485, 270], '0', 'Level', (82, 175, 46))
        self.trade_button = ImageButton(world, [600, 50], 'images/cell.9.png', [50, 50],
                                        front='images/orange_arrows.png', square=45)
        self.x_button = ImageButton(self.world, [420, 10], 'images/red_cell.9.png', [28, 28],
                                    front='images/x.png', square=22)
        self.change_visible(False)
        self.change_clickable(False)

    def change_visible(self, is_visible=None):
        if is_visible:
            change = is_visible
        else:
            change = not self.is_visible
        self.is_visible = change
        self.stage.change_visible(change)
        self.arrow.change_visible(change)
        self.level.change_visible(change)
        self.trade_button.change_visible(change)
        self.x_button.change_visible(change)

    def change_clickable(self, is_clickable=None):
        if is_clickable:
            change = is_clickable
        else:
            change = not self.is_clickable
        self.is_clickable = change
        self.stage.change_clickable(change)
        self.arrow.change_clickable(change)
        self.level.change_clickable(change)
        self.trade_button.change_clickable(change)
        self.x_button.change_clickable(change)

    def update_player(self, player):
        self.player = player
        self.level = Label(self.world, [485, 270], str(self.player.level), 'Level', (82, 175, 46))

    def draw_object(self):
        if self.is_visible:
            NinePatch.draw_object(self)
            self.stage.draw_object()
            if self.is_visible:
                player_pos = [475, 146]
                if self.player:
                    self.world.draw(self.player.surface, player_pos)
                    for i in self.player.items:
                        if i.is_used:
                            self.world.draw(i.surface, [player_pos[0] + i.item_pos[0], player_pos[1] + i.item_pos[1]])
                    self.world.draw(self.player.text_object.surface, [475, 225])
            self.x_button.draw_object()
            self.trade_button.draw_object()
            self.arrow.draw_object()
            self.level.draw_object()
