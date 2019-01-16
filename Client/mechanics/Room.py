from MapObject import MapObject
from Player import Player
from Client.mechanics.AStar.Search import search_path

from Screen import Screen


class Room(Screen):
    def __init__(self, world, room_id, bg_image, path, out):
        Screen.__init__(self, world, room_id, bg_image)
        self.path = MapObject(self.world, [0, 0], image=path, size=world.SIZE, is_transparent=True)
        self.out = out
        self.players = []
        for i in self.world.client.find_players(room_id):
            self.players.append(Player(world, data=self.world.client.player_info(i)))

    def execute(self):
        update = self.world.client.updates
        if not update or not update['headers'] or not update['headers']['username']:
            return
        print update
        for i in update['headers']['username']:
            for j in self.players:
                if i == j.username:
                    j.pos = update['data']['pos']
            i.check_message()
            i.walk()

    def check_event(self, event, objects=None):
        if objects is None:
            objects = []
        Screen.check_event(self, event, [self.path] + self.players + objects)

    def draw_screen(self, objects=None):
        if objects is None:
            objects = []
        Screen.draw_screen(self, [self.path] + self.players + objects)

    def on_click(self, map_object, event):
        raise NotImplementedError

    def on_type(self, map_object, event):
        raise NotImplementedError
