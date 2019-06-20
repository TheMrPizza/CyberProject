from Resources import colors, fonts
from MapObject import MapObject
from ImageButton import ImageButton
from NinePatch import NinePatch
from Label import Label
from ScrollBar import ScrollBar
from ShopItem import ShopItem


class ShopMenu(NinePatch):
    def __init__(self, world):
        NinePatch.__init__(self, world, [None, -10], 'images/elements/light_blue_cell.9.png', [500, 340], layer=8,
                           middle=world.cur_screen.bg_image)
        self.coins = Label(self.world, [312, 260], str(self.world.cur_player.coins), fonts['Compressed'],
                           colors['coins'])
        self.coin_image = MapObject(self.world,
                                    [312 + fonts['Compressed'].size(str(self.world.cur_player.coins))[0] + 2, 273],
                                    image='images/elements/coin.png', square=25)
        self.x_button = ImageButton(self.world, [295, 5], 'images/elements/light_red_color.9.png', [30, 30],
                                    image='images/elements/white_x.png', square=18)

        self.items = ScrollBar(self.world, [415, 5], 5, True, [360, 315])
        self.items.append(ShopItem(self.world, 11, 1000))
        self.items.append(ShopItem(self.world, 12, 1000))
        self.items.append(ShopItem(self.world, 41, 1500))
        self.items.append(ShopItem(self.world, 51, 3000))
        self.items.append(ShopItem(self.world, 71, 400))
        self.items.append(ShopItem(self.world, 72, 400))
        self.items.append(ShopItem(self.world, 73, 400))

        self.change_visible(False)
        self.change_clickable(False)

    def change_visible(self, is_visible=None):
        if is_visible is not None:
            change = is_visible
        else:
            change = not self.is_visible
        self.is_visible = change
        self.coins.change_visible(change)
        self.coin_image.change_visible(change)
        self.x_button.change_visible(change)
        self.items.change_visible(change)

    def change_clickable(self, is_clickable=None):
        if is_clickable is not None:
            change = is_clickable
        else:
            change = not self.is_clickable
        self.is_clickable = change
        self.coins.change_clickable(change)
        self.coin_image.change_clickable(change)
        self.x_button.change_clickable(change)
        self.items.change_clickable(change)

    def draw_object(self):
        if self.is_visible:
            NinePatch.draw_object(self)
            player_pos = [312, 150]
            self.world.draw(self.world.cur_player.surface, player_pos)
            for i in self.world.cur_player.items:
                if i.is_used:
                    self.world.draw(i.surface, [player_pos[0] + i.item_pos[0], player_pos[1] + i.item_pos[1]])
            self.world.draw(self.world.cur_player.text_object.surface, [312, 224])
            self.coins.draw_object()
            self.coin_image.draw_object()
            self.x_button.draw_object()
            self.items.draw_object()
