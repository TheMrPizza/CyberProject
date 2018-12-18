from MapObject import MapObject

from Screen import Screen


class Room(Screen):
    def __init__(self, world, room_id, bg_image, path, out):
        Screen.__init__(self, world, room_id, bg_image)
        self.path = MapObject(self.world, [0, 0], image=path, size=world.SIZE, is_transparent=True)
        self.out = out
        self.players = []

    def execute(self):
        for i in self.players:
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
