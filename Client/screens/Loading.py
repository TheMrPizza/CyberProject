from Client.mechanics.Screen import Screen
from Client.mechanics.Player import Player
from Beach import Beach
from Submarine import Submarine
from Forest import Forest
from Plaza import Plaza
from Market import Market
from Mountain import Mountain
from random import randint
import threading


class Loading(Screen):
    def __init__(self, world, cur_id, next_id, player_data=None):
        self.id = randint(0, 2)
        Screen.__init__(self, world, id, 'images/elements/loading_screen_' + str(self.id) + '.png')
        self.cur_id = cur_id
        self.next_id = next_id
        self.player_data = player_data
        self.room = None
        self.thread = threading.Thread(target=self.load_room)
        self.thread.start()

    def load_room(self):
        print self.cur_id, self.next_id
        if self.player_data:
            info = self.world.client.player_info(self.player_data)
            print 'Info received'
            self.world.cur_player = Player(self.world, info)
            self.next_id = self.world.cur_player.room_id
        if self.next_id == 201:
            if self.cur_id in [202, 301]:
                self.world.cur_player.update_pos([743, 343])
                self.world.client.update_player_pos(self.world.cur_player.username, self.world.cur_player.pos)
            elif self.cur_id == 203:
                self.world.cur_player.update_pos([23, 303])
                self.world.client.update_player_pos(self.world.cur_player.username, self.world.cur_player.pos)
            elif self.cur_id == 206:
                self.world.cur_player.update_pos([963, 163])
                self.world.client.update_player_pos(self.world.cur_player.username, self.world.cur_player.pos)
            self.room = Beach(self.world)
        elif self.next_id == 202:
            if self.cur_id in [201, 301]:
                self.world.cur_player.update_pos([23, 3])
                self.world.client.update_player_pos(self.world.cur_player.username, self.world.cur_player.pos)
            self.room = Submarine(self.world)
        elif self.next_id == 203:
            if self.cur_id in [201, 301]:
                self.world.cur_player.update_pos([1003, 503])
                self.world.client.update_player_pos(self.world.cur_player.username, self.world.cur_player.pos)
            elif self.cur_id == 204:
                self.world.cur_player.update_pos([303, 83])
                self.world.client.update_player_pos(self.world.cur_player.username, self.world.cur_player.pos)
            elif self.cur_id == 205:
                self.world.cur_player.update_pos([963, 103])
                self.world.client.update_player_pos(self.world.cur_player.username, self.world.cur_player.pos)
            self.room = Forest(self.world)
        elif self.next_id == 204:
            if self.cur_id in [203, 301]:
                self.world.cur_player.update_pos([43, 483])
                self.world.client.update_player_pos(self.world.cur_player.username, self.world.cur_player.pos)
            elif self.cur_id == 205:
                self.world.cur_player.update_pos([163, 163])
                self.world.client.update_player_pos(self.world.cur_player.username, self.world.cur_player.pos)
            elif self.cur_id == 206:
                self.world.cur_player.update_pos([783, 123])
                self.world.client.update_player_pos(self.world.cur_player.username, self.world.cur_player.pos)
            self.room = Plaza(self.world)
        elif self.next_id == 205:
            if self.cur_id in [203, 301]:
                self.world.cur_player.update_pos([23, 343])
                self.world.client.update_player_pos(self.world.cur_player.username, self.world.cur_player.pos)
            elif self.cur_id == 204:
                self.world.cur_player.update_pos([963, 323])
                self.world.client.update_player_pos(self.world.cur_player.username, self.world.cur_player.pos)
            self.room = Market(self.world)
        elif self.next_id == 206:
            if self.cur_id in [201, 301]:
                self.world.cur_player.update_pos([23, 383])
                self.world.client.update_player_pos(self.world.cur_player.username, self.world.cur_player.pos)
            elif self.cur_id == 204:
                self.world.cur_player.update_pos([963, 383])
                self.world.client.update_player_pos(self.world.cur_player.username, self.world.cur_player.pos)
            self.room = Mountain(self.world)
        if not self.player_data:
            self.world.client.add_player(self.room.screen_id, self.world.cur_player.username)

    def execute(self):
        if not self.thread.is_alive():  # Thread finished to create the room
            self.world.cur_screen = self.room

    def on_click(self, map_object, event):
        pass

    def on_type(self, map_object, event):
        pass

    def layer_reorder(self):
        pass
