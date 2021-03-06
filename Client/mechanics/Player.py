from Resources import colors, fonts, jon_missions, charles_missions
from MapObject import MapObject
from SpeechBalloon import SpeechBalloon
from Item import Item


class Player(MapObject):
    def __init__(self, world, data):
        if data:
            # Data sent from the server
            MapObject.__init__(self, world, data['pos'], image='images/items/' + str(data['body']) + '.png', layer=5)
            self.username = data['username']
            self.items = []
            if 'items' in data:
                for i in data['items']:
                    self.items.append(Item(self.world, self.world.client.item_info(i), self.pos,
                                           data['items'][i]['amount'], data['items'][i]['is_used']))
            self.level = data['level']
            self.missions = {}
            if 'missions' in data:
                self.missions = data['missions']
            if int(self.level) >= 3:
                self.update_mission(charles_missions[2][0][0], False)
            if int(self.level) >= 5:
                self.update_mission(charles_missions[2][1][0], False)
            if int(self.level) >= 10:
                self.update_mission(charles_missions[2][2][0], False)
            self.coins = data['coins']
            self.xp = data['xp']
            self.join_date = data['join_date']
            self.is_admin = data['is_admin']
            self.room_id = data['room_id']
            self.walking_path = []
            self.path_target = None
            self.msg = None
            self.balloon = None
            self.text_object = MapObject(world, [None, self.pos[1] + 75],
                                         fonts['Username'].render(self.username, True, colors['black']),
                                         middle=self, layer=6)

    def walk(self):
        if self.walking_path:
            pos = self.walking_path.pop()
            pos = [pos[0] - self.width / 2, pos[1] - self.height]
            self.update_pos(pos)
            self.world.cur_screen.layer_reorder()

            if not self.walking_path:  # Path ended
                if self.path_target == 0:
                    self.world.cur_screen.players.remove(self)
                elif self.path_target:  # Player is going out of the room
                    from Client.screens.Loading import Loading
                    self.world.cur_screen = Loading(self.world, self.world.cur_screen.screen_id, self.path_target)
                    self.path_target = None

    def update_pos(self, pos):
        self.text_object.pos[0] += pos[0] - self.pos[0]
        self.text_object.pos[1] += pos[1] - self.pos[1]
        for i in self.items:
            i.pos = pos
        self.pos = pos
        if self.balloon:
            self.balloon.update(pos)

    def add_item(self, item_id):
        for i in self.items:
            if i.item_id == str(item_id):
                i.amount += 1
                return
        self.items.append(Item(self.world, self.world.client.item_info(item_id), self.pos, 1, False))

    def check_mission(self, mission_id):
        if str(mission_id) in self.missions:
            return self.missions[str(mission_id)]
        return None

    def update_mission(self, mission_id, value):
        # Check that the mission is relevant
        if not value and str(mission_id) in self.missions:
            return
        if mission_id % 10 != 0:
            if str(mission_id - 1) not in self.missions:
                return
            if not self.missions[str(mission_id - 1)]:
                return

        if str(mission_id) in self.missions:
            if self.missions[str(mission_id)] != value:
                self.missions[str(mission_id)] = value
                self.world.client.update_mission(self.username, mission_id, value)
        else:
            self.missions[str(mission_id)] = value
            self.world.client.update_mission(self.username, mission_id, value)

    def check_message(self):
        if self.msg:
            self.update_mission(jon_missions[2][0][0], False)
            if self.room_id == 201:
                self.world.cur_screen.agent_menu.update_missions()
            self.balloon = SpeechBalloon(self.world, self.pos, self.msg)
            self.msg = None
        elif self.balloon and not self.balloon.is_alive:
            self.balloon = None

    def get_all_items(self):
        items = []
        for i in self.items:
            for j in xrange(i.amount):
                items.append(i)
        return items

    def change_item(self, item):
        if item.is_used:
            item.is_used = False
        else:
            for i in self.items:
                if i.type == item.type and i.is_used:
                    i.is_used = False
                    if self is self.world.cur_player:
                        self.world.client.change_item(self.username, i.item_id)
            item.is_used = True
        if self is self.world.cur_player:
            self.world.client.change_item(self.username, item.item_id)

    def draw_object(self):
        MapObject.draw_object(self)
        for i in self.items:
            i.draw_object()
        self.text_object.draw_object()
        if self.balloon:
            self.balloon.draw_object()

    def on_type(self, event):
        pass
