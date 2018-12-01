from MapObject import MapObject


class Player(MapObject):
    def __init__(self, world, username, is_male, items, level, join_date, is_admin, room_id, pos):
        MapObject.__init__(self, world, pos, image='images/player.png')
        self.username = username
        self.is_male = is_male
        self.items = items
        self.level = level
        self.join_date = join_date
        self.is_admin = is_admin
        self.room_id = room_id
        self.path = []

    def walk(self):
        if self.path:
            pos = self.path.pop()
            self.pos = pos[0] - self.width / 2, pos[1] - self.height / 2
            self.world.cur_screen.layer_reorder()

    def on_type(self, event):
        pass
