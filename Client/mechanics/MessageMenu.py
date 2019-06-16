from NinePatch import NinePatch
from Label import Label
from TextButton import TextButton
from MapObject import MapObject


class MessageMenu(NinePatch):
    def __init__(self, world, title, text, xp='0', items='0', coins='0', is_warning=False):
        if is_warning:
            NinePatch.__init__(self, world, [None, 100], 'images/elements/light_red_box.9.png', [600, 250], middle=world.cur_screen.bg_image, layer=10)
            self.button = TextButton(self.world, [None, 300], 'images/elements/white_color.9.png', [75, 35], 'OK',
                                     'Regular', (219, 76, 76), middle=self, layer=11)
        else:
            NinePatch.__init__(self, world, [None, 100], 'images/elements/light_blue_box.9.png', [600, 250], middle=world.cur_screen.bg_image, layer=10)
            self.button = TextButton(self.world, [None, 300], 'images/elements/white_color.9.png', [75, 35], 'OK',
                                     'Regular', (41, 182, 246), middle=self, layer=11)
        self.title = Label(self.world, [None, 95], title, 'Title', (255, 255, 255), middle=self, layer=11)
        self.msg = Label(self.world, [None, 160], text, 'Regular', (255, 255, 255), middle=self, layer=11)
        self.xp, self.items, self.coins = None, None, None
        if xp != '0' and items != '0' and coins != '0':
            self.xp = Label(self.world, [300, 220], str(xp) + ' XP', 'Compressed', (21, 101, 192), layer=11)
            self.items = MapObject(self.world, [None, 215], image='images/items/' + str(items) + '.png', middle=self, layer=11)
            self.coins = Label(self.world, [700, 220], str(coins), 'Compressed', (253, 216, 53), layer=11)
            self.coin_image = MapObject(self.world, [700 + self.world.fonts['Compressed'].size(str(coins))[0] + 2, 235], image='images/elements/coin.png', square=25, layer=11)
        elif xp != '0' and coins != '0':
            self.xp = Label(self.world, [470, 220], str(xp) + ' XP', 'Compressed', (21, 101, 192), layer=11)
            self.coins = Label(self.world, [550, 220], str(coins), 'Compressed', (253, 216, 53), layer=11)
            self.coin_image = MapObject(self.world,
                                        [550 + self.world.fonts['Compressed'].size(str(coins))[0] + 2, 235],
                                        image='images/elements/coin.png', square=25, layer=11)
        elif xp != '0':
            self.xp = Label(self.world, [None, 220], str(xp) + ' XP', 'Compressed', (21, 101, 192), middle=self, layer=11)
        self.world.client.add_rewards(self.world.cur_player.username, xp, items, coins)
        self.change_visible(False)
        self.change_clickable(False)

    def change_visible(self, is_visible=None):
        if is_visible is not None:
            change = is_visible
        else:
            change = not self.is_visible
        self.is_visible = change
        self.title.change_visible(change)
        self.msg.change_visible(change)
        if self.xp:
            self.xp.change_visible(change)
        if self.items:
            self.items.change_visible(change)
        if self.coins:
            self.coins.change_visible(change)
            self.coin_image.change_visible(change)
        self.button.change_visible(change)

    def change_clickable(self, is_clickable=None):
        if is_clickable is not None:
            change = is_clickable
        else:
            change = not self.is_clickable
        self.is_clickable = change
        self.title.change_clickable(change)
        self.msg.change_clickable(change)
        if self.xp:
            self.xp.change_clickable(change)
        if self.items:
            self.items.change_clickable(change)
        if self.coins:
            self.coins.change_clickable(change)
            self.coin_image.change_clickable(change)
        self.button.change_clickable(change)

    def draw_object(self):
        if self.is_visible:
            NinePatch.draw_object(self)
            self.title.draw_object()
            self.msg.draw_object()
            if self.xp:
                self.xp.draw_object()
            if self.items:
                self.items.draw_object()
            if self.coins:
                self.coins.draw_object()
                self.coin_image.draw_object()
            self.button.draw_object()
