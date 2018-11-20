from Screen import Screen


class Room(Screen):
    def __init__(self, room_id, bg_image, path, out):
        Screen.__init__(self, room_id, bg_image)
        self.path = path
        self.out = out
        self.players = []


