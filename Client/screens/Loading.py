from Client.mechanics.Screen import Screen
from Client.mechanics.Player import Player
from Beach import Beach
from Submarine import Submarine
from random import randint
import threading


class Loading(Screen):
    def __init__(self, world, room_id, player_data=None):
        self.id = 0 #randint(0, 5)
        Screen.__init__(self, world, id, 'images/loading_screen_' + str(self.id) + '.png')
        self.room_id = room_id
        self.player_data = player_data
        self.room = None
        self.thread = threading.Thread(target=self.load_room)
        self.thread.start()

    def load_room(self):
        if self.player_data:
            info = self.world.client.player_info(self.player_data)
            print 'Info received'
            self.world.cur_player = Player(self.world, info)
            print '1'
            self.room_id = self.world.cur_player.room_id
        if self.room_id == 201:
            if not self.player_data:
                self.world.client.update_player_pos(self.world.cur_player.username, [780, 380])
            print '1.5'
            self.room = Beach(self.world)
            print '2'
        elif self.room_id == 202:
            if not self.player_data:
                self.world.client.update_player_pos(self.world.cur_player.username, [20, 0])
            self.room = Submarine(self.world)

        if not self.player_data:
            self.world.client.add_player(self.room.screen_id, self.world.cur_player.username)
        print '3'

    def execute(self):
        if not self.thread.is_alive():  # Thread finished to create the room
            self.world.cur_screen = self.room

    def on_click(self, map_object, event):
        pass

    def on_type(self, map_object, event):
        pass

    def layer_reorder(self):
        pass
