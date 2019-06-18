from Client.mechanics.Resources import jenny_missions
from Client.mechanics.MapObject import MapObject
from Client.mechanics.AStar.Search import search_path
from Client.mechanics.Room import Room
from Client.mechanics.ShopMenu import ShopMenu
from Client.mechanics.MessageMenu import MessageMenu


class Market(Room):
    def __init__(self, world):
        Room.__init__(self, world, 205, 'images/rooms/205/market.png', 'images/rooms/205/path.png', [])
        self.out = [MapObject(self.world, [0, 0], image='images/rooms/205/out1.png', is_visible=False, layer=7),
                    MapObject(self.world, [0, 0], image='images/rooms/205/out2.png', is_visible=False, layer=7)]
        self.hut1 = MapObject(self.world, [10, 490], image='images/rooms/205/hut1.png', layer=3)
        self.hut2 = MapObject(self.world, [293, 515], image='images/rooms/205/hut2.png', layer=3)
        self.hut3 = MapObject(self.world, [580, 505], image='images/rooms/205/hut3.png', layer=3)
        self.hut4 = MapObject(self.world, [850, 488], image='images/rooms/205/hut4.png', layer=3)
        self.hut5 = MapObject(self.world, [None, 32], image='images/rooms/205/hut5.png', middle=self.bg_image, layer=3)
        self.shop_menu = ShopMenu(self.world)
        self.layer_reorder()

    def check_event(self, event, objects=None):
        if objects is None:
            objects = []
        buttons = [i.button for i in self.shop_menu.items.items]
        Room.check_event(self, event, buttons + [self.hut1, self.hut2, self.hut3, self.hut4, self.hut5, self.shop_menu, self.shop_menu.x_button] + objects)

    def check_scroll(self, event, objects=None):
        if objects is None:
            objects = []
        Room.check_scroll(self, event, [self.shop_menu] + objects)

    def draw_screen(self, objects=None):
        if objects is None:
            objects = []
        Room.draw_screen(self, [self.hut1, self.hut2, self.hut3, self.hut4, self.hut5, self.shop_menu] + objects)

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
                    self.world.cur_player.path_target = 203
                elif map_object is self.out[1]:
                    self.world.cur_player.path_target = 204
                else:
                    self.world.cur_player.path_target = None
            return
        if map_object is self.hut5:
            self.shop_menu.change_visible(True)
            self.shop_menu.change_clickable(True)
            return
        if map_object is self.shop_menu.x_button:
            self.shop_menu.change_visible(False)
            self.shop_menu.change_clickable(False)
            return
        for i in self.shop_menu.items.items:
            if map_object is i.button:
                if i.item_id == 41:
                    self.world.cur_player.update_mission(jenny_missions[0][0][0], False)
                self.message_menu = MessageMenu(self.world, "It's Look Great!", 'You bought a new item from the shop:', 500, i.item_id, -i.price)
                self.message_menu.change_visible()
                self.message_menu.change_clickable()
                return
        Room.on_click(self, map_object, event)

    def on_scroll(self, map_object, event):
        if map_object is self.shop_menu:
            self.shop_menu.items.scroll(event.button == 4)
            return
        Room.on_scroll(self, map_object, event)

    def layer_reorder(self):
        objects = self.players + [self.hut1, self.hut2, self.hut3, self.hut4]
        objects = sorted(objects, key=lambda o: o.pos[1] + o.height)
        for i in xrange(len(objects)):
            objects[i].layer = i+2

    def on_type(self, map_object, event):
        if map_object is self.chat_box:
            data = map_object.on_type(event)
            if data:
                map_object.on_send(data)
