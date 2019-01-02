from MapObject import MapObject

from SpeechBalloon import SpeechBalloon


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
        self.walking_path = []
        self.msg = None
        self.balloon = None

    def walk(self):
        if self.walking_path:
            pos = self.walking_path.pop()
            self.pos = pos[0] - self.width / 2, pos[1] - self.height / 2
            self.world.cur_screen.layer_reorder()

    def check_message(self):
        if self.msg:
            self.balloon = SpeechBalloon(self.world, [self.pos[0] + 40, self.pos[1] - 60], self.msg)
            self.msg = None
        elif self.balloon:
            self.balloon.update([self.pos[0] + 40, self.pos[1] - 60])
            if not self.balloon.is_alive:
                self.balloon = None

    def draw_object(self):
        self.world.draw(self.surface, self.pos)
        if self.balloon:
            self.balloon.draw_object()

    def on_type(self, event):
        pass
