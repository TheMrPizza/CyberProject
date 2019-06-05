from Client.mechanics.MapObject import MapObject
from Client.mechanics.AStar.Search import search_path
from Client.mechanics.Room import Room


class Forest(Room):
    def __init__(self, world):
        Room.__init__(self, world, 203, 'images/rooms/203/forest.png', 'images/rooms/203/path.png', [])
        self.tree = MapObject(self.world, [20, 0], image='images/rooms/203/tree.png', layer=4)
        self.bush1 = MapObject(self.world, [5, 465], image='images/rooms/203/bush1.png', layer=4)
        self.bush2 = MapObject(self.world, [950, 200], image='images/rooms/203/bush2.png', layer=4)
        self.trunk = MapObject(self.world, [430, 305], image='images/rooms/203/trunk.png', layer=4)
        self.sign = MapObject(self.world, [820, 470], image='images/rooms/203/sign.png', layer=4)

        self.out = [MapObject(self.world, [0, 0], image='images/rooms/203/out1.png', is_visible=False, layer=7),
                    MapObject(self.world, [0, 0], image='images/rooms/203/out2.png', is_visible=False, layer=7),
                    MapObject(self.world, [0, 0], image='images/rooms/203/out3.png', is_visible=False, layer=7)]
        self.layer_reorder()

    def check_event(self, event, objects=None):
        if objects is None:
            objects = []
        Room.check_event(self, event, [self.tree, self.bush1, self.bush2, self.trunk, self.sign, self.chat_box] + objects)

    def draw_screen(self, objects=None):
        if objects is None:
            objects = []
        Room.draw_screen(self, [self.tree, self.bush1, self.bush2, self.trunk, self.sign, self.chat_box] + objects)

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
                    self.world.cur_player.path_target = 201
                elif map_object is self.out[1]:
                    pass  # self.world.cur_player.path_target = 205
                elif map_object is self.out[2]:
                    self.world.cur_player.path_target = 204
        Room.on_click(self, map_object, event)

    def layer_reorder(self):
        objects = self.players + [self.tree, self.bush2, self.trunk, self.sign]
        objects = sorted(objects, key=lambda o: o.pos[1] + o.height)
        for i in xrange(len(objects)):
            objects[i].layer = i+2

    def on_type(self, map_object, event):
        if map_object is self.chat_box:
            data = map_object.on_type(event)
            if data:
                map_object.on_send(data)
