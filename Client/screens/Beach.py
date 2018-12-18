from Client.mechanics.MapObject import MapObject

from Client.mechanics.AStar.Search import search_path
from Client.mechanics.Room import Room
from Client.mechanics.TextBox import TextBox


class Beach(Room):
    def __init__(self, world):
        Room.__init__(self, world, 201, 'test_map.png', 'test_path.png', [])
        self.bush = MapObject(self.world, [606, 192], image='test_bush.png', layer=3)
        self.bush_shadow = MapObject(self.world, [self.bush.pos[0], self.bush.pos[1] + 42],
                                     image='test_bush_shadow.png', layer=1)
        self.chat_box = TextBox(self.world, [None, 540], 720, middle=self.bg_image)

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
                path = search_path(self.world, (self.players[0].pos[0] + self.players[0].width / 2,
                                                self.players[0].pos[1] + self.players[0].height / 2), event.pos)
                if path:
                    self.players[0].walking_path = path

    def layer_reorder(self):
        for i in self.players:
            if self.bush.pos[1] + self.bush.height < i.pos[1] + i.height:
                self.bush.layer = 2
                i.layer = 3
            else:
                i.layer = 2
                self.bush.layer = 3

    def on_type(self, map_object, event):
        if map_object is self.chat_box:
            map_object.on_type(event)
