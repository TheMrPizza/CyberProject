from Client.mechanics.Resources import colors, fonts
from Client.mechanics.MapObject import MapObject
from Client.mechanics.AStar.Search import search_path
from Client.mechanics.Room import Room
from Client.mechanics.Label import Label
from Client.mechanics.AgentMenu import AgentMenu
from Client.mechanics.MessageMenu import MessageMenu


class Beach(Room):
    def __init__(self, world):
        Room.__init__(self, world, 201, 'images/rooms/201/beach.png', 'images/rooms/201/path.png', [])
        self.out = [MapObject(self.world, [852, 380], image='images/rooms/201/submarine_entrance.png', layer=7),
                    MapObject(self.world, [0, 0], image='images/rooms/201/out1.png', is_visible=False, layer=7),
                    MapObject(self.world, [0, 0], image='images/rooms/201/out2.png', is_visible=False, layer=7)]
        self.jon = MapObject(self.world, [315, 65], image='images/rooms/201/jon.png', layer=3)
        self.name = Label(self.world, [None, 170], 'Jon', fonts['NPC'], colors['jon'], middle=self.jon)
        self.agent_menu = AgentMenu(self.world, 'Jon')
        self.layer_reorder()

    def check_event(self, event, objects=None):
        if objects is None:
            objects = []
        buttons = []
        for i in self.agent_menu.missions.items:
            buttons.append(i.button)
            buttons.append(i.reward_button)
        Room.check_event(self, event, buttons + [self.jon, self.agent_menu, self.agent_menu.x_button] + objects)

    def draw_screen(self, objects=None):
        if objects is None:
            objects = []
        Room.draw_screen(self, [self.jon, self.name, self.agent_menu] + objects)

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
                    self.world.cur_player.path_target = 202
                elif map_object is self.out[1]:
                    self.world.cur_player.path_target = 206
                elif map_object is self.out[2]:
                    self.world.cur_player.path_target = 203
                else:
                    self.world.cur_player.path_target = None
            return
        if map_object is self.jon:
            self.agent_menu.change_visible(True)
            self.agent_menu.change_clickable(True)
            return
        if map_object is self.agent_menu.x_button:
            self.agent_menu.change_visible(False)
            self.agent_menu.change_clickable(False)
            return
        for i in self.agent_menu.missions.items:
            if map_object is i.button:
                i.change_state()
                self.agent_menu.missions.update_items()
                return
            if map_object is i.reward_button:
                if i.is_completed:
                    self.world.cur_screen.message_menu = MessageMenu(self.world, 'Mission Completed!',
                                                                     'You have completed the mission and got the next'
                                                                     ' rewards:',
                                                                     i.xp, i.items, i.coins)
                    self.world.cur_player.update_mission(i.mission_id, True)
                    self.agent_menu.update_missions()
                return
        Room.on_click(self, map_object, event)

    def check_scroll(self, event, objects=None):
        if objects is None:
            objects = []
        Room.check_scroll(self, event, [self.agent_menu.missions] + objects)

    def layer_reorder(self):
        objects = self.players + [self.jon]
        objects = sorted(objects, key=lambda o: o.pos[1] + o.height)
        for i in xrange(len(objects)):
            objects[i].layer = i+2

    def on_type(self, map_object, event):
        if map_object is self.chat_box:
            data = map_object.on_type(event)
            if data:
                map_object.on_send(data)

    def on_scroll(self, map_object, event):
        if map_object is self.agent_menu.missions:
            self.agent_menu.missions.scroll(event.button == 4)
            return
        Room.on_scroll(self, map_object, event)
