from Client.mechanics.MapObject import MapObject
from Client.mechanics.AStar.Search import search_path
from Client.mechanics.Room import Room
from Client.mechanics.Label import Label


class Forest(Room):
    def __init__(self, world):
        Room.__init__(self, world, 203, 'images/rooms/203/forest.png', 'images/rooms/203/path.png', [])
        self.out = [MapObject(self.world, [0, 0], image='images/rooms/203/out1.png', is_visible=False, layer=7),
                    MapObject(self.world, [0, 0], image='images/rooms/203/out2.png', is_visible=False, layer=7),
                    MapObject(self.world, [0, 0], image='images/rooms/203/out3.png', is_visible=False, layer=7)]
        self.tree = MapObject(self.world, [20, 0], image='images/rooms/203/tree.png', layer=3)
        self.bush1 = MapObject(self.world, [5, 465], image='images/rooms/203/bush1.png', layer=3)
        self.bush2 = MapObject(self.world, [950, 200], image='images/rooms/203/bush2.png', layer=3)
        self.trunk = MapObject(self.world, [430, 305], image='images/rooms/203/trunk.png', layer=3)
        self.sign = MapObject(self.world, [820, 470], image='images/rooms/203/sign.png', layer=3)
        self.jenny = MapObject(self.world, [562, 108], image='images/rooms/203/jenny.png', layer=3)
        self.name = Label(self.world, [None, 210], 'Jenny', 'NPC', (197, 53, 74), middle=self.jenny)
        self.layer_reorder()

    def check_event(self, event, objects=None):
        if objects is None:
            objects = []
        Room.check_event(self, event,
                         [self.tree, self.bush1, self.bush2, self.trunk, self.sign, self.jenny] + objects)

    def draw_screen(self, objects=None):
        if objects is None:
            objects = []
        Room.draw_screen(self, [self.tree, self.bush1, self.bush2, self.trunk, self.sign, self.jenny, self.name] + objects)

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
                    self.world.cur_player.path_target = 205
                elif map_object is self.out[2]:
                    self.world.cur_player.path_target = 204
                else:
                    self.world.cur_player.path_target = None
        Room.on_click(self, map_object, event)

    def layer_reorder(self):
        objects = self.players + [self.tree, self.bush2, self.trunk, self.sign, self.jenny]
        objects = sorted(objects, key=lambda o: o.pos[1] + o.height)
        for i in xrange(len(objects)):
            objects[i].layer = i+2

    def on_type(self, map_object, event):
        if map_object is self.chat_box:
            data = map_object.on_type(event)
            if data:
                map_object.on_send(data)
