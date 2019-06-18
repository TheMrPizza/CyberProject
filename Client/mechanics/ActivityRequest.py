import pygame
from Resources import colors, fonts
from NinePatch import NinePatch
from ImageButton import ImageButton
from MapObject import MapObject
from Label import Label


class ActivityRequest(NinePatch):
    def __init__(self, world, activity, player, is_incoming):
        NinePatch.__init__(self, world, [0, 0], 'images/elements/light_blue_box.9.png', [180, 60], layer=8)
        self.ttl = 10000  # ms
        self.activity = activity
        self.player = player
        self.is_incoming = is_incoming
        self.buttons = {}
        if self.activity == 'TRADE':
            self.icon = MapObject(self.world, [10, None], image='images/elements/white_opposite_arrows.png', square=40, middle=self)
        elif self.activity == 'XO':
            self.icon = MapObject(self.world, [10, None], image='images/elements/white_xo.png', square=40, middle=self)

        self.label = Label(self.world, [62, None], self.player.username, fonts['Username'], colors['white'], middle=self)

        if self.is_incoming:
            self.buttons['v'] = ImageButton(self.world, [152, 8], 'images/elements/light_green_color.9.png', [20, 20],
                                            image='images/elements/white_v.png', square=15)
            self.buttons['x'] = ImageButton(self.world, [152, 32], 'images/elements/light_red_color.9.png', [20, 20],
                                            image='images/elements/white_x.png', square=11)
        else:
            self.buttons['x'] = ImageButton(self.world, [152, None], 'images/elements/light_red_color.9.png', [20, 20],
                                            image='images/elements/white_x.png', square=11, middle=self)
        self.is_deleted = False
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
        self.label.pos[0] += pos[0] - self.pos[0]
        self.label.pos[1] += pos[1] - self.pos[1]
        for i in self.buttons:
            self.buttons[i].update_pos([self.buttons[i].pos[0] + pos[0] - self.pos[0],
                                        self.buttons[i].pos[1] + pos[1] - self.pos[1]])
        self.pos = pos

    def decline_request(self):
        NinePatch.__init__(self, self.world, self.pos, 'images/elements/light_red_box.9.png', [180, 60],
                           layer=8)
        self.buttons = {}
        self.is_deleted = True
        self.ttl = 3000  # ms
        self.start_time = pygame.time.get_ticks()

    def draw_object(self):
        if self.is_visible:
            if pygame.time.get_ticks() - self.start_time >= self.ttl:
                if self.is_deleted:
                    self.world.cur_screen.activity_requests.remove(self)
                    return
                else:
                    self.world.client.activity_response(self.activity, self.player.username,
                                                        self.world.cur_player.username, 'x')
                    self.decline_request()
            NinePatch.draw_object(self)
            self.icon.draw_object()
            self.label.draw_object()
            for i in self.buttons:
                self.buttons[i].draw_object()

    def draw_item(self, surface):
        if self.is_visible:
            if pygame.time.get_ticks() - self.start_time >= self.ttl:
                if self.is_deleted:
                    self.world.cur_screen.activity_requests.remove(self)
                    return
                else:
                    self.world.client.activity_response(self.activity, self.player.username,
                                                        self.world.cur_player.username, 'x')
                    self.decline_request()
            surface.blit(self.surface, self.pos)
            for i in self.buttons:
                self.buttons[i].draw_item(surface)
            surface.blit(self.icon.surface, self.icon.pos)
            surface.blit(self.label.surface, self.label.pos)
