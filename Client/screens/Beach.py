from Client.mechanics.MapObject import MapObject
from Client.mechanics.AStar.Search import search_path
from Client.mechanics.Room import Room
from Client.mechanics.TextBox import TextBox
from Client.screens.Submarine import Submarine


class Beach(Room):
    def __init__(self, world):
        Room.__init__(self, world, 201, 'images/test_map.png', 'images/test_path.png', [])
        self.bush = MapObject(self.world, [606, 192], image='images/test_bush.png', layer=3)
        self.bush_shadow = MapObject(self.world, [self.bush.pos[0], self.bush.pos[1] + 42],
                                     image='images/test_bush_shadow.png', layer=1)
        self.chat_box = TextBox(self.world, [None, 540], 720, middle=self.bg_image)
        self.out.append(MapObject(self.world, [800, 400], image='images/submarine_enterance.png', layer=2))

    def check_event(self, event, objects=None):
        if objects is None:
            objects = []
        Room.check_event(self, event, [self.bush, self.bush_shadow, self.chat_box] + objects)

    def draw_screen(self, objects=None):
        if objects is None:
            objects = []
        Room.draw_screen(self, [self.bush, self.bush_shadow, self.chat_box] + objects)

    def on_click(self, map_object, event):
        if map_object is self.path:
            if self.path.surface.get_at(event.pos).a != 0:
                path = search_path(self.world, (self.world.cur_player.pos[0] + self.world.cur_player.width / 2,
                                                self.world.cur_player.pos[1] + self.world.cur_player.height / 2), event.pos)
                if path:
                    self.world.cur_player.walking_path = path
                    self.world.client.update_player_pos(self.world.cur_player.username, [event.pos[0] - self.world.cur_player.width/2,
                                                                                         event.pos[1] - self.world.cur_player.height/2])
        elif map_object in self.out:
            room = Submarine(self.world)
            self.world.client.add_player(room.screen_id, self.world.cur_player.username)
            self.world.cur_screen = room

    def layer_reorder(self):
        objects = self.players + [self.bush]
        objects = sorted(objects, key=lambda o: o.pos[1] + o.height)
        for i in xrange(len(objects)):
            objects[i].layer = i+2

    def on_type(self, map_object, event):
        if map_object is self.chat_box:
            data = map_object.on_type(event)
            if data:
                map_object.on_send(data)
