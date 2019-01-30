from Client.mechanics.MapObject import MapObject
from Client.mechanics.AStar.Search import search_path
from Client.mechanics.Room import Room
from Client.mechanics.TextBox import TextBox


class Submarine(Room):
    def __init__(self, world):
        Room.__init__(self, world, 202, 'images/submarine.png', 'images/submarine_path.png', [])
        self.chat_box = TextBox(self.world, [None, 540], 720, middle=self.bg_image)
        self.out.append(MapObject(self.world, [20, -30], image='images/ladder.png', layer=2))

    def check_event(self, event, objects=None):
        if objects is None:
            objects = []
        Room.check_event(self, event, [self.chat_box] + objects)

    def draw_screen(self, objects=None):
        if objects is None:
            objects = []
        Room.draw_screen(self, [self.chat_box] + objects)

    def on_click(self, map_object, event):
        if map_object in [self.path] + self.out:
            if self.path.surface.get_at(event.pos).a != 0:
                path = search_path(self.world, (self.world.cur_player.pos[0] + self.world.cur_player.width / 2,
                                                self.world.cur_player.pos[1] + self.world.cur_player.height / 2), event.pos)
                if path:
                    self.world.cur_player.walking_path = path
                    self.world.client.update_player_pos(self.world.cur_player.username, [event.pos[0] - self.world.cur_player.width/2,
                                                                                         event.pos[1] - self.world.cur_player.height/2])
                    if map_object in self.out:
                        self.world.cur_player.path_target = 201

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