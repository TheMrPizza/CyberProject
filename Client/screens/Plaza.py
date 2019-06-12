from Client.mechanics.MapObject import MapObject
from Client.mechanics.AStar.Search import search_path
from Client.mechanics.Room import Room


class Plaza(Room):
    def __init__(self, world):
        Room.__init__(self, world, 204, 'images/rooms/204/plaza.png', 'images/rooms/204/path.png', [])
        self.gate1 = MapObject(self.world, [775, 18], image='images/rooms/204/gate1.png', layer=4)
        self.gate2 = MapObject(self.world, [110, 38], image='images/rooms/204/gate2.png', layer=4)
        self.sign = MapObject(self.world, [185, 440], image='images/rooms/204/sign.png', layer=4)

        self.out = [MapObject(self.world, [0, 0], image='images/rooms/204/out1.png', is_visible=False, layer=7),
                    MapObject(self.world, [0, 0], image='images/rooms/204/out2.png', is_visible=False, layer=7),
                    MapObject(self.world, [0, 0], image='images/rooms/204/out3.png', is_visible=False, layer=7)]
        self.layer_reorder()

    def check_event(self, event, objects=None):
        if objects is None:
            objects = []
        Room.check_event(self, event, [self.gate1, self.gate2, self.sign, self.chat_box] + objects)

    def draw_screen(self, objects=None):
        if objects is None:
            objects = []
        Room.draw_screen(self, [self.gate1, self.gate2, self.sign, self.chat_box] + objects)

    def on_click(self, map_object, event):
        if map_object in [self.path] + self.out:
            path = search_path(self.world, (self.world.cur_player.pos[0] + self.world.cur_player.width / 2,
                                            self.world.cur_player.pos[1] + self.world.cur_player.height),
                               event.pos)
            if path:
                self.world.cur_player.walking_path = path
                self.world.client.update_player_pos(self.world.cur_player.username,
                                                    [event.pos[0] - self.world.cur_player.width / 2,
                                                     event.pos[1] - self.world.cur_player.height / 2])
                if map_object is self.out[0]:
                    self.world.cur_player.path_target = 203
                elif map_object is self.out[1]:
                    self.world.cur_player.path_target = 206
                elif map_object is self.out[2]:
                    self.world.cur_player.path_target = 205
        Room.on_click(self, map_object, event)

    def layer_reorder(self):
        objects = self.players + [self.sign, self.gate1, self.gate2]
        objects = sorted(objects, key=lambda o: o.pos[1] + o.height)
        for i in xrange(len(objects)):
            objects[i].layer = i+2

    def on_type(self, map_object, event):
        if map_object is self.chat_box:
            data = map_object.on_type(event)
            if data:
                map_object.on_send(data)
