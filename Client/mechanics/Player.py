from MapObject import MapObject
from SpeechBalloon import SpeechBalloon


class Player(MapObject):
    def __init__(self, world, data):
        if data:
            # Another player. Data sent from the server
            MapObject.__init__(self, world, data['pos'], image='images/player.png')
            self.username = data['username']
            self.is_male = data['is_male']
            self.items = data['items']
            self.level = data['level']
            self.join_date = data['join_date']
            self.is_admin = data['is_admin']
            self.room_id = data['room_id']
            self.walking_path = []
            self.path_target = None
            self.msg = None
            self.balloon = None
            self.text_object = MapObject(world, [None, self.pos[1] + 75],
                                         self.world.fonts['Username'].render(self.username, False, (0, 0, 0)), middle=self, layer=6)

    def walk(self):
        if self.walking_path:
            pos = self.walking_path.pop()
            pos = [pos[0] - self.width / 2, pos[1] - self.height / 2]
            self.update_pos(pos)
            self.world.cur_screen.layer_reorder()
            if not self.walking_path:  # Path ended
                if self.path_target:  # Player is going out of the room
                    if self.path_target == 201:  # TODO: Fix
                        self.world.cur_player.update_pos([780, 380])
                        self.world.cur_screen.layer_reorder()
                        from Client.screens.Beach import Beach
                        room = Beach(self.world)
                        self.world.client.add_player(room.screen_id, self.world.cur_player.username)
                        self.world.cur_screen = room
                    if self.path_target == 202:
                        self.world.cur_player.update_pos([20, 0])
                        self.world.cur_screen.layer_reorder()
                        from Client.screens.Submarine import Submarine
                        room = Submarine(self.world)
                        self.world.client.add_player(room.screen_id, self.world.cur_player.username)
                        self.world.cur_screen = room

    def update_pos(self, pos):
        self.text_object.pos[0] += pos[0] - self.pos[0]
        self.text_object.pos[1] += pos[1] - self.pos[1]
        self.pos = pos
        if self.balloon:
            self.balloon.update(pos)

    def check_message(self):
        if self.msg:
            self.balloon = SpeechBalloon(self.world, self.pos, self.msg)
            self.msg = None
        elif self.balloon and not self.balloon.is_alive:
            self.balloon = None

    def draw_object(self):
        self.world.draw(self.surface, self.pos)
        self.world.draw(self.text_object.surface, self.text_object.pos)
        if self.balloon:
            self.balloon.draw_object()

    def on_type(self, event):
        pass
