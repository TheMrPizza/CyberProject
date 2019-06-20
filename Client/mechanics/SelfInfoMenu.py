from Resources import colors, fonts
from MapObject import MapObject
from ImageButton import ImageButton
from NinePatch import NinePatch
from Label import Label


class SelfInfoMenu(NinePatch):
    def __init__(self, world):
        NinePatch.__init__(self, world, [None, -10], 'images/elements/light_blue_cell.9.png', [480, 340], layer=8,
                           middle=world.cur_screen.bg_image)
        self.stage = MapObject(world, [323, -10], image='images/elements/stage.png', layer=9)
        self.coins = Label(self.world, [310, 265], str(self.world.cur_player.coins), fonts['Compressed'],
                           colors['coins'])
        self.coin_image = MapObject(self.world,
                                    [310 + fonts['Compressed'].size(str(self.world.cur_player.coins))[0] + 2, 278],
                                    image='images/elements/coin.png', square=25)
        self.xp = Label(self.world, [385, 265], str(self.world.cur_player.xp) + ' XP', fonts['Compressed'],
                        colors['dark_blue'])
        self.level = Label(self.world, [465, 265], str(self.world.cur_player.level), fonts['Compressed'],
                           colors['level'], layer=9)
        self.arrow = MapObject(self.world, [465 + fonts['Compressed'].size(str(self.world.cur_player.level))[0] + 2,
                                            277], image='images/elements/level_arrow.png', square=27, layer=9)
        self.x_button = ImageButton(self.world, [303, 5], 'images/elements/light_red_color.9.png', [30, 30],
                                    image='images/elements/white_x.png', square=18)
        self.cells = []
        for i in xrange(5):
            for j in xrange(4):
                if len(self.world.cur_player.get_all_items()) > 4 * i + j:
                    self.cells.append([self.world.cur_player.get_all_items()[4 * i + j].item_id,
                                      ImageButton(self.world, [513 + j * 63, 5 + i * 63],
                                                  'images/elements/light_blue_color.9.png', [58, 58],
                                                  image='images/items/' +
                                                        self.world.cur_player.get_all_items()[4 * i + j].item_id +
                                                        '.png', square=50)])
                else:
                    self.cells.append([-1, ImageButton(self.world, [513 + j * 63, 5 + i * 63],
                                                       'images/elements/light_blue_color.9.png', [58, 58])])
        self.change_visible(False)
        self.change_clickable(False)

    def change_visible(self, is_visible=None):
        if is_visible is not None:
            change = is_visible
        else:
            change = not self.is_visible
        self.is_visible = change
        self.stage.change_visible(change)
        self.coins.change_visible(change)
        self.coin_image.change_visible(change)
        self.xp.change_visible(change)
        self.arrow.change_visible(change)
        self.level.change_visible(change)
        self.x_button.change_visible(change)
        for i in self.cells:
            i[1].change_visible(change)

    def change_clickable(self, is_clickable=None):
        if is_clickable is not None:
            change = is_clickable
        else:
            change = not self.is_clickable
        self.is_clickable = change
        self.stage.change_clickable(change)
        self.coins.change_clickable(change)
        self.coin_image.change_clickable(change)
        self.xp.change_clickable(change)
        self.arrow.change_clickable(change)
        self.level.change_clickable(change)
        self.x_button.change_clickable(change)
        for i in self.cells:
            i[1].change_clickable(change)

    def draw_object(self):
        if self.is_visible:
            NinePatch.draw_object(self)
            self.stage.draw_object()
            if self.is_visible:
                player_pos = [368, 146]
                self.world.draw(self.world.cur_player.surface, player_pos)
                for i in self.world.cur_player.items:
                    if i.is_used:
                        self.world.draw(i.surface, [player_pos[0] + i.item_pos[0], player_pos[1] + i.item_pos[1]])
                self.world.draw(self.world.cur_player.text_object.surface, [368, 220])
            self.x_button.draw_object()
            self.coins.draw_object()
            self.coin_image.draw_object()
            self.xp.draw_object()
            self.arrow.draw_object()
            self.level.draw_object()
            for i in self.cells:
                i[1].draw_object()
