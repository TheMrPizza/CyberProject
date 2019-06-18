from Resources import colors, fonts
from NinePatch import NinePatch
from Label import Label
from ImageButton import ImageButton
from MapObject import MapObject
from TextButton import TextButton
from SpeechBalloon import SpeechBalloon


class MissionItem(NinePatch):
    def __init__(self, world, mission_id, title, text, xp, items='0', coins=0, is_completed=False):
        if is_completed:
            NinePatch.__init__(self, world, [0, 0], 'images/elements/light_green_box.9.png', [550, 50], layer=8)
            self.button = ImageButton(self.world, [8, None], 'images/elements/white_color.9.png', [35, 35],
                                      'images/elements/light_green_plus.png', square=25, middle=self, layer=9)
        else:
            NinePatch.__init__(self, world, [0, 0], 'images/elements/light_blue_box.9.png', [550, 50], layer=8)
            self.button = ImageButton(self.world, [8, None], 'images/elements/light_green_color.9.png', [35, 35],
                                      'images/elements/white_plus.png', square=25, middle=self, layer=9)
        self.mission_id = mission_id
        self.xp = xp
        self.items = items
        self.coins = coins
        self.is_completed = is_completed
        self.text = SpeechBalloon.size_adjustment(text, fonts['Little'], 520)
        self.lines = SpeechBalloon.create_lines(self.world, [None, 50], self.text, fonts['Little'], self, colors['white'])
        self.title = Label(self.world, [51, None], title, fonts['Medium'], colors['white'], middle=self)
        self.reward_button = TextButton(self.world, [None, self.lines[-1].pos[1] + self.lines[-1].height + 5], 'images/elements/white_color.9.png', [125, 35], 'Claim Reward',
                                    fonts['Regular'], (76, 219, 110), middle=self, layer=11)
        self.reward_button.change_visible(False)
        self.reward_button.change_clickable(False)
        if self.items == '0':
            self.xp_label = Label(self.world, [400, None], str(xp) + ' XP', fonts['Compressed'], colors['dark_blue'], middle=self, layer=11)
        else:
            self.xp_label = Label(self.world, [300, None], str(xp) + ' XP', fonts['Compressed'], colors['dark_blue'], middle=self, layer=11)
            self.items_image = MapObject(self.world, [380, None], image='images/items/' + str(items) + '.png', middle=self,
                                         layer=9)
        self.coins_label = Label(self.world, [490, None], str(coins), fonts['Compressed'], colors['coins'], middle=self)
        self.coin_image = MapObject(self.world,
                                    [490 + fonts['Compressed'].size(str(coins))[0] + 2, None],
                                    image='images/elements/coin.png', middle=self, square=25)
        self.is_expanded = False

    def change_state(self):
        if self.is_expanded:  # Contract
            if self.is_completed:
                NinePatch.__init__(self, self.world, self.pos, 'images/elements/light_green_box.9.png', [550, 50], layer=8)
                self.button.change_front('images/elements/light_green_plus.png', square=25)
                self.reward_button.change_visible(False)
                self.reward_button.change_clickable(False)
            else:
                NinePatch.__init__(self, self.world, self.pos, 'images/elements/light_blue_box.9.png', [550, 50], layer=8)
                self.button.change_bg('images/elements/light_green_color.9.png', [35, 35])
                self.button.change_front('images/elements/white_plus.png', square=25)
            for i in self.lines:
                i.change_visible(False)
            self.is_expanded = False
        else:  # Expand
            if self.is_completed:
                height = self.reward_button.pos[1] + self.reward_button.height - self.pos[1] + 10
                NinePatch.__init__(self, self.world, self.pos, 'images/elements/light_green_box.9.png', [550, height], layer=8)
                self.button.change_front('images/elements/light_red_minus.png', square=25)
                self.reward_button.change_visible(True)
                self.reward_button.change_clickable(True)
            else:
                height = self.lines[-1].pos[1] + self.lines[-1].height - self.pos[1] + 5
                NinePatch.__init__(self, self.world, self.pos, 'images/elements/light_blue_box.9.png', [550, height], layer=8)
                self.button.change_bg('images/elements/light_red_color.9.png', [35, 35])
                self.button.change_front('images/elements/white_minus.png', square=25)
            for i in self.lines:
                i.change_visible(True)
            self.is_expanded = True

    def change_visible(self, is_visible=None):
        if is_visible is not None:
            change = is_visible
        else:
            change = not self.is_visible
        self.is_visible = change
        for i in self.lines:
            i.change_visible(change)
        self.button.change_visible(change)
        self.title.change_visible(change)
        if change:
            if self.is_completed and self.is_expanded:
                self.reward_button.change_visible(change)
        else:
            self.reward_button.change_visible(change)
        self.xp_label.change_visible(change)
        if self.items != '0':
            self.items_image.change_visible(change)
        self.coins_label.change_visible(change)
        self.coin_image.change_visible(change)

    def change_clickable(self, is_clickable=None):
        if is_clickable is not None:
            change = is_clickable
        else:
            change = not self.is_clickable
        self.is_clickable = change
        for i in self.lines:
            i.change_clickable(change)
        self.button.change_clickable(change)
        self.title.change_clickable(change)
        if change:
            if self.is_completed and self.is_expanded:
                self.reward_button.change_clickable(change)
        else:
            self.reward_button.change_clickable(change)
        self.xp_label.change_clickable(change)
        if self.items != '0':
            self.items_image.change_clickable(change)
        self.coins_label.change_clickable(change)
        self.coin_image.change_clickable(change)

    def update_pos(self, pos):
        self.button.update_pos([self.button.pos[0] + pos[0] - self.pos[0],
                                self.button.pos[1] + pos[1] - self.pos[1]])
        for i in self.lines:
            i.pos[0] += pos[0] - self.pos[0]
            i.pos[1] += pos[1] - self.pos[1]
        self.title.pos[0] += pos[0] - self.pos[0]
        self.title.pos[1] += pos[1] - self.pos[1]
        self.reward_button.update_pos([self.reward_button.pos[0] + pos[0] - self.pos[0],
                                       self.reward_button.pos[1] + pos[1] - self.pos[1]])
        self.xp_label.pos[0] += pos[0] - self.pos[0]
        self.xp_label.pos[1] += pos[1] - self.pos[1]
        if self.items != '0':
            self.items_image.pos[0] += pos[0] - self.pos[0]
            self.items_image.pos[1] += pos[1] - self.pos[1]
        self.coins_label.pos[0] += pos[0] - self.pos[0]
        self.coins_label.pos[1] += pos[1] - self.pos[1]
        self.coin_image.pos[0] += pos[0] - self.pos[0]
        self.coin_image.pos[1] += pos[1] - self.pos[1]
        self.pos = pos

    def draw_object(self):
        if self.is_visible:
            NinePatch.draw_object(self)
            if self.is_expanded:
                for i in self.lines:
                    i.draw_object()
                if self.is_completed:
                    self.reward_button.draw_object()
            self.button.draw_object()
            self.title.draw_object()
            self.xp_label.draw_object()
            if self.items != '0':
                self.items_image.draw_object()
            self.coins_label.draw_object()
            self.coin_image.draw_object()

    def draw_item(self, surface):
        if self.is_visible:
            surface.blit(self.surface, self.pos)
            if self.is_expanded:
                for i in self.lines:
                    surface.blit(i.surface, i.pos)
                if self.is_completed:
                    self.reward_button.draw_item(surface)
            self.button.draw_item(surface)
            surface.blit(self.title.surface, self.title.pos)
            surface.blit(self.xp_label.surface, self.xp_label.pos)
            if self.items != '0':
                surface.blit(self.items_image.surface, self.items_image.pos)
            surface.blit(self.coins_label.surface, self.coins_label.pos)
            surface.blit(self.coin_image.surface, self.coin_image.pos)
