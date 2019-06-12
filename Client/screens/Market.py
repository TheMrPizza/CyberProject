from Client.mechanics.MapObject import MapObject
from Client.mechanics.AStar.Search import search_path
from Client.mechanics.Room import Room


class Market(Room):
    def __init__(self, world):
        Room.__init__(self, world, 205, 'images/rooms/205/market.png', 'images/rooms/205/path.png', [])
        self.hut1 = MapObject(self.world, [10, 490], image='images/rooms/205/hut1.png', layer=4)
        self.hut2 = MapObject(self.world, [293, 515], image='images/rooms/205/hut2.png', layer=4)
        self.hut3 = MapObject(self.world, [580, 505], image='images/rooms/205/hut3.png', layer=4)
        self.hut4 = MapObject(self.world, [850, 488], image='images/rooms/205/hut4.png', layer=4)

        self.out = [MapObject(self.world, [0, 0], image='images/rooms/205/out1.png', is_visible=False, layer=7),
                    MapObject(self.world, [0, 0], image='images/rooms/205/out2.png', is_visible=False, layer=7)]
        self.layer_reorder()

    def check_event(self, event, objects=None):
        if objects is None:
            objects = []
        Room.check_event(self, event, [self.hut1, self.hut2, self.hut3, self.hut4, self.chat_box] + objects)

    def draw_screen(self, objects=None):
        if objects is None:
            objects = []
        Room.draw_screen(self, [self.hut1, self.hut2, self.hut3, self.hut4, self.chat_box] + objects)

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
                    self.world.cur_player.path_target = 204
        Room.on_click(self, map_object, event)

    def layer_reorder(self):
        objects = self.players + [self.hut1, self.hut2, self.hut3, self.hut4]
        objects = sorted(objects, key=lambda o: o.pos[1] + o.height)
        for i in xrange(len(objects)):
            objects[i].layer = i+2

    def on_type(self, map_object, event):
        if map_object is self.chat_box:
            data = map_object.on_type(event)
            if data:
                map_object.on_send(data)
