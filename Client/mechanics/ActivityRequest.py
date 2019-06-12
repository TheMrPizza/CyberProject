import pygame
from NinePatch import NinePatch
from ImageButton import ImageButton
from MapObject import MapObject


class ActivityRequest(NinePatch):
    def __init__(self, world, activity, player, is_incoming):
        NinePatch.__init__(self, world, [20, 20], 'images/test_text_box.9.png', [180, 60], layer=8)
        self.TTL = 10000  # ms
        self.activity = activity
        self.player = player
        self.is_incoming = is_incoming
        self.buttons = {}
        if self.activity == 'TRADE':
            self.icon = MapObject(self.world, [30, None], image='images/orange_arrows.png', size=[40, 40], square=40, middle=self)
        else:
            self.icon = MapObject(self.world, [30, None], image='images/xo.png', size=[40, 40], square=40, middle=self)

        if self.is_incoming:
            self.buttons['v'] = ImageButton(world, [160, 30], 'images/green_cell.9.png', [20, 20], image='images/v.png', square=15)
            self.buttons['x'] = ImageButton(world, [160, 50], 'images/red_cell.9.png', [20, 20], image='images/x.png', square=15)
        else:
            self.buttons['x'] = ImageButton(world, [160, 40], 'images/red_cell.9.png', [20, 20], image='images/x.png', square=15)
        self.start_time = pygame.time.get_ticks()

    def change_visible(self, is_visible=None):
        if is_visible:
            change = is_visible
        else:
            change = not self.is_visible
        self.is_visible = change
        self.icon.change_visible(change)
        for i in self.buttons:
            self.buttons[i].change_visible(change)

    def change_clickable(self, is_clickable=None):
        if is_clickable:
            change = is_clickable
        else:
            change = not self.is_clickable
        self.is_clickable = change
        self.icon.change_clickable(change)
        for i in self.buttons:
            self.buttons[i].change_clickable(change)

    def update_pos(self, pos):
        self.icon.pos[0] += pos[0] - self.pos[0]
        self.icon.pos[1] += pos[1] - self.pos[1]
        for i in self.buttons:
            self.buttons[i].update_pos([pos[0] + self.buttons[i].pos[0] - self.pos[0],
                                        pos[1] + self.buttons[i].pos[1] - self.pos[1]])
        self.pos = pos

    def draw_object(self):
        if self not in self.world.cur_screen.activity_requests:
            del self
        if self.is_visible:
            if pygame.time.get_ticks() - self.start_time >= self.TTL:
                self.world.client.activity_response(self.activity, self.player.username, self.world.cur_player.username, 'x')
                self.world.cur_screen.activity_requests.remove(self)
            NinePatch.draw_object(self)
            self.icon.draw_object()
            self.world.draw(self.player.text_object.surface, [self.pos[0] + 60, self.pos[1] + 20])
            for i in self.buttons:
                self.buttons[i].draw_object()
