from NinePatch import NinePatch
from Label import Label
from TextButton import TextButton
from MapObject import MapObject
from Item import Item


class ShopItem(NinePatch):
    def __init__(self, world, item_id, price):
        self.item_id = item_id
        self.price = price
        if price > world.cur_player.coins:
            NinePatch.__init__(self, world, [0, 0], 'images/elements/light_red_box.9.png', [360, 80], layer=8)
            self.button = TextButton(self.world, [280, 40], 'images/elements/white_color.9.png', [75, 35], 'Buy',
                                     'Regular', (219, 76, 76), middle=self, layer=9)
        else:
            NinePatch.__init__(self, world, [0, 0], 'images/elements/light_blue_box.9.png', [360, 80], layer=8)
            self.button = TextButton(self.world, [280, 40], 'images/elements/white_color.9.png', [75, 35], 'Buy',
                                     'Regular', (41, 182, 246), middle=self, layer=9)
        self.item = Item(self.world, self.world.client.item_info(self.item_id), [10, None], 1, True, middle=self)
        self.title = Label(self.world, [None, None], self.item.title, 'Medium', (255, 255, 255), middle=self)
        self.coins = Label(self.world, [287, -4], str(self.price), 'Compressed', (253, 216, 53))
        self.coin_image = MapObject(self.world,
                                    [287 + self.world.fonts['Compressed'].size(str(self.price))[0] + 2, 9],
                                    image='images/elements/coin.png', square=25)

    def change_visible(self, is_visible=None):
        if is_visible is not None:
            change = is_visible
        else:
            change = not self.is_visible
        self.is_visible = change
        self.button.change_visible(change)
        self.item.change_visible(change)
        self.title.change_visible(change)
        self.coins.change_visible(change)
        self.coin_image.change_visible(change)

    def change_clickable(self, is_clickable=None):
        if is_clickable is not None:
            change = is_clickable
        else:
            change = not self.is_clickable
        self.is_clickable = change
        self.button.change_clickable(change)
        self.item.change_clickable(change)
        self.title.change_clickable(change)
        self.coins.change_clickable(change)
        self.coin_image.change_clickable(change)

    def update_pos(self, pos):
        self.button.update_pos([self.button.pos[0] + pos[0] - self.pos[0],
                                self.button.pos[1] + pos[1] - self.pos[1]])
        self.item.pos[0] += pos[0] - self.pos[0]
        self.item.pos[1] += pos[1] - self.pos[1]
        self.title.pos[0] += pos[0] - self.pos[0]
        self.title.pos[1] += pos[1] - self.pos[1]
        self.coins.pos[0] += pos[0] - self.pos[0]
        self.coins.pos[1] += pos[1] - self.pos[1]
        self.coin_image.pos[0] += pos[0] - self.pos[0]
        self.coin_image.pos[1] += pos[1] - self.pos[1]
        self.pos = pos

    def draw_object(self):
        if self.is_visible:
            NinePatch.draw_object(self)
            self.button.draw_object()
            self.item.draw_object(False)
            self.title.draw_object()
            self.coins.draw_object()
            self.coin_image.draw_object()

    def draw_item(self, surface):
        if self.is_visible:
            surface.blit(self.surface, self.pos)
            self.button.draw_item(surface)
            surface.blit(self.item.surface, self.item.pos)
            surface.blit(self.title.surface, self.title.pos)
            surface.blit(self.coins.surface, self.coins.pos)
            surface.blit(self.coin_image.surface, self.coin_image.pos)
