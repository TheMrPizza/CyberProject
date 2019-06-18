from Client.mechanics.Resources import jon_missions
from Client.mechanics.MapObject import MapObject
from Client.mechanics.AStar.Search import search_path
from Client.mechanics.Room import Room


class Submarine(Room):
    def __init__(self, world):
        Room.__init__(self, world, 202, 'images/rooms/202/submarine.png', 'images/rooms/202/path.png', [])
        self.out = [MapObject(self.world, [0, 0], image='images/rooms/202/out1.png', is_visible=False, layer=7)]
        self.world.cur_player.update_mission(jon_missions[0][0][0], False)
        self.layer_reorder()

    def check_event(self, event, objects=None):
        if objects is None:
            objects = []
        Room.check_event(self, event, objects)

    def draw_screen(self, objects=None):
        if objects is None:
            objects = []
        Room.draw_screen(self, objects)

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
                else:
                    self.world.cur_player.path_target = None
            return
        Room.on_click(self, map_object, event)

    def layer_reorder(self):
        objects = self.players
        objects = sorted(objects, key=lambda o: o.pos[1] + o.height)
        for i in xrange(len(objects)):
            objects[i].layer = i+2

    def on_type(self, map_object, event):
        if map_object is self.chat_box:
            data = map_object.on_type(event)
            if data:
                map_object.on_send(data)
