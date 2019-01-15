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
        print self.players
        for i in self.players:
            update = Player(self.world, data=self.world.client.player_info(i.username))
            if len(i.walking_path) != 0:
                path = search_path(self.world, (i.pos[0] + i.width / 2, i.pos[1] + i.height / 2), update.pos)
                if path:
                    i.walking_path = path
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
