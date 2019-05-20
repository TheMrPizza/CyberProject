from MapObject import MapObject
from Client.mechanics.TextBox import TextBox
from Client.mechanics.ImageButton import ImageButton
from Client.mechanics.SelfInfoMenu import SelfInfoMenu
from Client.mechanics.PlayerInfoMenu import PlayerInfoMenu
from Client.mechanics.ActivityRequest import ActivityRequest
from TradeMenu import TradeMenu
from XOMenu import XOMenu
from Player import Player
from Client.mechanics.AStar.Search import search_path
from Screen import Screen
from Item import Item


class Room(Screen):
    def __init__(self, world, room_id, bg_image, path, out):
        Screen.__init__(self, world, room_id, bg_image)
        self.path = MapObject(self.world, [0, 0], image=path, size=world.SIZE, is_visible=False)
        self.out = out
        self.chat_box = TextBox(self.world, [None, 540], 720, middle=self.bg_image)
        self.bag_button = ImageButton(self.world, [900, 540], 'images/test_text_box.9.png', [50, 50], 'images/bag.png')
        self.bag = MapObject(self.world, [600, 540], image='images/bag.png')
        self.self_info_menu = SelfInfoMenu(world)
        self.player_info_menu = PlayerInfoMenu(world)
        self.activity_requests = []
        self.trade_menu = TradeMenu(world)
        self.xo_menu = XOMenu(world)

        self.world.cur_player = Player(world, data=self.world.client.player_info(self.world.cur_player.username))
        self.players = [self.world.cur_player]
        for i in self.world.client.find_players(room_id):
            if i != self.world.cur_player.username:
                self.players.append(Player(world, data=self.world.client.player_info(i)))

    def execute(self):
        update = self.world.client.updates
        for i in update:
            if i['code'] == 'POS':
                for j in self.players:
                    if i['headers']['username'] == j.username:
                        pos = [int(i['data'].split(' ')[0]) + j.width / 2, int(i['data'].split(' ')[1]) + j.height / 2]
                        path = search_path(self.world, (j.pos[0] + j.width / 2, j.pos[1] + j.height / 2), pos)
                        j.walking_path = path
                        update.remove(i)
                        break
            elif i['code'] == 'CONNECT':
                info = self.world.client.player_info(i['headers']['username'])
                self.players.append(Player(self.world, info))
                update.remove(i)
            elif i['code'] == 'QUIT':
                print 'someone quited'
                for j in self.players:
                    if i['headers']['username'] == j.username:
                        self.players.remove(j)
                        update.remove(i)
                        break
            elif i['code'] == 'CHAT':
                for j in self.players:
                    if i['headers']['username'] == j.username:
                        j.msg = i['headers']['message']
                        update.remove(i)
                        break
            elif i['code'] == 'ADD PLAYER':
                info = self.world.client.player_info(i['headers']['username'])
                self.players.append(Player(self.world, data=info))
                update.remove(i)
            elif i['code'] == 'REMOVE PLAYER':
                for j in self.players:
                    if i['headers']['username'] == j.username:
                        self.players.remove(j)
                        update.remove(i)
                        break
            elif i['code'] == 'CHANGE ITEM':
                for j in self.players:
                    if i['headers']['username'] == j.username:
                        for k in j.items:
                            if k.item_id == i['headers']['item_id']:
                                j.change_item(k)
                                break
                        update.remove(i)
                        break
            elif i['code'] == 'ACTIVITY REQUEST':
                for j in self.players:
                    if i['headers']['sender'] == j.username:
                        self.activity_requests.append(ActivityRequest(self.world, i['headers']['activity'], j, True))
                        update.remove(i)
                        break
            elif i['code'] == 'ACTIVITY RESPONSE':
                for j in self.activity_requests:
                    if j.player.username == i['headers']['addressee']:
                        self.activity_requests.remove(j)
                        if i['headers']['is_accepted'] == 'v':
                            if i['headers']['activity'] == 'TRADE':
                                self.player_info_menu.change_visible(False)
                                self.player_info_menu.change_clickable(False)
                                self.self_info_menu.change_visible(False)
                                self.self_info_menu.change_clickable(False)
                                self.trade_menu.player = j.player
                                self.trade_menu.change_visible()
                                self.trade_menu.change_clickable()
                            elif i['headers']['activity'] == 'XO':
                                self.player_info_menu.change_visible(False)
                                self.player_info_menu.change_clickable(False)
                                self.self_info_menu.change_visible(False)
                                self.self_info_menu.change_clickable(False)
                                self.xo_menu.player = j.player
                                self.xo_menu.letter = 'X'
                                self.xo_menu.change_visible()
                                self.xo_menu.change_clickable()
                        break
                update.remove(i)
            elif i['code'] == 'PLACE ITEM':
                self.trade_menu.player_place_item(i['headers']['item'])
                update.remove(i)
            elif i['code'] == 'REMOVE ITEM':
                self.trade_menu.player_remove_item(int(i['headers']['index']))
                update.remove(i)
            elif i['code'] == 'ACCEPT TRADE':
                self.trade_menu.player_accept_trade()
                update.remove(i)
            elif i['code'] == 'DECLINE TRADE':
                self.trade_menu.change_visible()
                self.trade_menu.change_clickable()
                self.trade_menu.player = None
                self.trade_menu = TradeMenu(self.world)
                update.remove(i)
            elif i['code'] == 'MAKE TRADE':
                for j in self.players:
                    if i['headers']['user1'] == j.username:
                        for k in j.items:
                            if k.item_id in i['headers']['items1'].split():
                                if k.amount == 1:
                                    j.items.remove(k)
                                else:
                                    k.amount -= 1

                        for k in i['headers']['items2'].split():
                            is_found = False
                            for l in j.items:
                                if l.item_id == k:
                                    is_found = True
                                    l.amount += 1
                            if not is_found:
                                j.items.append(Item(self.world, self.world.client.item_info(k), j.pos, 1, False))
                    elif i['headers']['user2'] == j.username:
                        for k in j.items:
                            if k.item_id in i['headers']['items2'].split():
                                if k.amount == 1:
                                    j.items.remove(k)
                                else:
                                    k.amount -= 1
                        for k in i['headers']['items1'].split():
                            is_found = False
                            for l in j.items:
                                if l.item_id == k:
                                    is_found = True
                                    l.amount += 1
                            if not is_found:
                                j.items.append(Item(self.world, self.world.client.item_info(k), j.pos, 1, False))

                if self.world.cur_player.username in [i['headers']['user1'], i['headers']['user2']]:
                    self.world.cur_screen.self_info_menu = SelfInfoMenu(self.world)
                    self.trade_menu = TradeMenu(self.world)
                update.remove(i)

    def check_event(self, event, objects=None):
        if objects is None:
            objects = []

        buttons = []
        for i in self.activity_requests:
            for j in i.buttons:
                buttons.append(i.buttons[j])
        cells = []
        for i in self.xo_menu.cells:
            for j in i:
                cells.append(j[1])
        Screen.check_event(self, event, self.out + buttons + cells + list(zip(*self.self_info_menu.cells)[1]) +
                           list(zip(*self.trade_menu.all_cells)[1]) + list(zip(*self.trade_menu.self_cells)[1]) +
                           list(zip(*self.trade_menu.player_cells)[1]) +
                           [self.path, self.bag_button, self.self_info_menu.x_button, self.player_info_menu.x_button,
                            self.player_info_menu.trade_button, self.player_info_menu.xo_button,
                            self.trade_menu.v_button, self.trade_menu.x_button]
                           + self.players + objects)

    def draw_screen(self, objects=None):
        for i in self.players:
            i.walk()
            i.check_message()

        if objects is None:
            objects = []
        Screen.draw_screen(self, self.out + self.activity_requests + [self.path, self.bag_button, self.self_info_menu, self.player_info_menu, self.trade_menu, self.xo_menu] + self.players + objects)

    def on_click(self, map_object, event):
        if map_object in [self.bag_button, self.self_info_menu.x_button]:
            self.self_info_menu.change_visible()
            self.self_info_menu.change_clickable()
            return
        if map_object is self.player_info_menu.x_button:
            self.player_info_menu.change_visible()
            self.player_info_menu.change_clickable()
            return
        if map_object is self.player_info_menu.trade_button:
            self.world.client.activity_request('TRADE', self.world.cur_player.username, self.player_info_menu.player.username)
            self.activity_requests.append(ActivityRequest(self.world, 'TRADE', self.player_info_menu.player, False))
            return
        if map_object is self.player_info_menu.xo_button:
            self.world.client.activity_request('XO', self.world.cur_player.username, self.player_info_menu.player.username)
            self.activity_requests.append(ActivityRequest(self.world, 'XO', self.player_info_menu.player, False))
            return
        for i in self.activity_requests:
            for j in i.buttons:
                if map_object is i.buttons[j]:
                    self.world.client.activity_response(i.activity, i.player.username, self.world.cur_player.username, j)
                    self.activity_requests.remove(i)
                    if j == 'v':  # Start trading!
                        if i.activity == 'TRADE':
                            self.player_info_menu.change_visible(False)
                            self.player_info_menu.change_clickable(False)
                            self.self_info_menu.change_visible(False)
                            self.self_info_menu.change_clickable(False)
                            self.trade_menu.player = i.player
                            self.trade_menu.change_visible()
                            self.trade_menu.change_clickable()
                        elif i.activity == 'XO':
                            self.player_info_menu.change_visible(False)
                            self.player_info_menu.change_clickable(False)
                            self.self_info_menu.change_visible(False)
                            self.self_info_menu.change_clickable(False)
                            self.xo_menu.player = i.player
                            self.xo_menu.letter = 'O'
                            self.xo_menu.change_visible()
                            self.xo_menu.stage.pos = [650, -10]
                    return
        for i in self.players:
            if map_object is i and i is not self.world.cur_player:
                self.player_info_menu.update_player(i)
                self.player_info_menu.change_visible()
                self.player_info_menu.change_clickable()
                return
        for i in self.self_info_menu.cells:
            if map_object is i[1] and map_object.front:
                for j in self.world.cur_player.items:
                    if j.item_id == i[0]:
                        self.world.cur_player.change_item(j)
                        return
        for i in xrange(len(self.trade_menu.all_cells)):
            if map_object is self.trade_menu.all_cells[i][1] and map_object.front and not self.trade_menu.is_final:
                self.world.client.place_item(self.trade_menu.player.username, self.trade_menu.all_cells[i][0])
                self.trade_menu.place_item(i)
                return
        for i in xrange(len(self.trade_menu.self_cells)):
            if map_object is self.trade_menu.self_cells[i][1] and map_object.front and not self.trade_menu.is_final:
                self.trade_menu.remove_item(i)
                self.world.client.remove_item(self.trade_menu.player.username, i)
                return
        if map_object is self.trade_menu.v_button:
            self.trade_menu.accept_trade()
            return
        if map_object is self.trade_menu.x_button:
            self.world.client.decline_trade(self.trade_menu.player.username)
            self.trade_menu = TradeMenu(self.world)
            return
        for i in xrange(len(self.xo_menu.cells)):
            for j in xrange(len(self.xo_menu.cells[0])):
                if map_object is self.xo_menu.cells[i][j][1]:
                    self.xo_menu.play_turn(self.xo_menu.letter, i, j)
                    self.world.client.xo_turn()

    def on_type(self, map_object, event):
        raise NotImplementedError
