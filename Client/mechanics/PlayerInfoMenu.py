from Resources import colors, fonts
from MapObject import MapObject
from ImageButton import ImageButton
from NinePatch import NinePatch
from Label import Label


class PlayerInfoMenu(NinePatch):
    def __init__(self, world):
        NinePatch.__init__(self, world, [None, -10], 'images/elements/light_blue_cell.9.png', [300, 340], middle=world.cur_screen.bg_image, layer=8)
        self.player = None
        self.stage = MapObject(self.world, [430, -10], image='images/stage.png', layer=9)
        self.level = Label(self.world, [500, 265], '0', fonts['Compressed'], colors['level'], layer=9)
        self.arrow = MapObject(self.world, [500, 277], image='images/elements/level_arrow.png', square=27, layer=9)
        self.trade_button = ImageButton(self.world, [610, 50], 'images/elements/light_blue_color.9.png', [50, 50],
                                        image='images/elements/white_opposite_arrows.png', square=45)
        self.xo_button = ImageButton(self.world, [610, 120], 'images/elements/light_blue_color.9.png', [50, 50],
                                        image='images/elements/white_xo.png', square=45)
        self.x_button = ImageButton(self.world, [393, 5], 'images/elements/light_red_color.9.png', [30, 30], image='images/elements/white_x.png', square=18)
        self.change_visible(False)
        self.change_clickable(False)

    def change_visible(self, is_visible=None):
        if is_visible is not None:
            change = is_visible
        else:
            change = not self.is_visible
        self.is_visible = change
        self.stage.change_visible(change)
        self.arrow.change_visible(change)
        self.level.change_visible(change)
        self.trade_button.change_visible(change)
        self.xo_button.change_visible()
        self.x_button.change_visible(change)

    def change_clickable(self, is_clickable=None):
        if is_clickable is not None:
            change = is_clickable
        else:
            change = not self.is_clickable
        self.is_clickable = change
        self.stage.change_clickable(change)
        self.arrow.change_clickable(change)
        self.level.change_clickable(change)
        self.trade_button.change_clickable(change)
        self.xo_button.change_clickable()
        self.x_button.change_clickable(change)

    def update_player(self, player):
        self.player = player
        self.level = Label(self.world, [500, 265], str(self.player.level), fonts['Compressed'], colors['level'], layer=9)
        self.arrow = MapObject(self.world, [500 + fonts['Compressed'].size(str(self.player.level))[0] + 2, 277], image='images/elements/level_arrow.png', square=27, layer=9)

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
                    self.world.draw(self.player.text_object.surface, [475, 222])
            self.x_button.draw_object()
            self.trade_button.draw_object()
            self.xo_button.draw_object()
            self.arrow.draw_object()
            self.level.draw_object()
