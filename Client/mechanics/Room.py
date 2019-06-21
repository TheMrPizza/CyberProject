from Resources import jon_missions, jenny_missions, charles_missions
from MapObject import MapObject
from TextBox import TextBox
from ImageButton import ImageButton
from SelfInfoMenu import SelfInfoMenu
from PlayerInfoMenu import PlayerInfoMenu
from ActivityRequest import ActivityRequest
from ScrollBar import ScrollBar
from TradeMenu import TradeMenu
from XOMenu import XOMenu
from MapMenu import MapMenu
from MessageMenu import MessageMenu
from Player import Player
from Client.mechanics.AStar.Search import search_path
from Screen import Screen
from Item import Item


class Room(Screen):
    jon_mission = set()
    charles_mission = 0

    def __init__(self, world, room_id, bg_image, path, out):
        Screen.__init__(self, world, room_id, bg_image)
        self.path = MapObject(self.world, [0, 0], image=path, size=world.SIZE, is_visible=False, layer=0)
        self.out = out
        self.chat_box = TextBox(self.world, [None, 540], 720, middle=self.bg_image, layer=10)
        self.bag_button = ImageButton(self.world, [900, 540], 'images/elements/dark_blue_color.9.png', [43, 43],
                                      image='images/elements/white_person.png', square=33)
        self.map_button = ImageButton(self.world, [122, 540], 'images/elements/light_blue_color.9.png', [43, 43],
                                      image='images/elements/white_map.png', square=33)
        self.self_info_menu = SelfInfoMenu(world)
        self.player_info_menu = PlayerInfoMenu(world)
        self.activity_requests = ScrollBar(self.world, [20, 20], 5, True, [180, 100])
        self.trade_menu = TradeMenu(world)
        self.xo_menu = XOMenu(world)
        self.map_menu = MapMenu(world, room_id)
        self.message_menu = MessageMenu(self.world, '', '')
        self.message_menu.change_visible()
        self.message_menu.change_clickable()

        if self.world.cur_player.check_mission(jon_missions[0][0][0]):
            Room.jon_mission.add(room_id)
            if len(Room.jon_mission) == 6:
                self.world.cur_player.update_mission(jon_missions[0][1][0], False)

        self.players = [self.world.cur_player]
        for i in self.world.client.find_players(room_id):
            if i != self.world.cur_player.username:
                self.players.append(Player(world, data=self.world.client.player_info(i)))
        if len(self.players) >= 3:
            self.world.cur_player.update_mission(jon_missions[1][0][0], False)
        if len(self.players) >= 5:
            self.world.cur_player.update_mission(jon_missions[1][0][0], False)
        if len(self.players) >= 10:
            self.world.cur_player.update_mission(jon_missions[1][0][0], False)

    def execute(self):
        update = self.world.client.updates
        for i in update:
            if i['code'] == 'POS':
                for j in self.players:
                    if i['headers']['username'] == j.username:
                        pos = [int(i['data'].split(' ')[0]) + j.width / 2, int(i['data'].split(' ')[1]) + j.height / 2]
                        path = search_path(self.world, (j.pos[0] + j.width / 2, j.pos[1] + j.height), pos)
                        j.walking_path = path
                        is_found = False
                        for k in self.out:
                            if k.check_collision(pos):
                                if k.surface.get_at([pos[0] - k.pos[0], pos[1] - k.pos[1]]).a != 0:
                                    is_found = True
                                    j.path_target = 0
                                    break
                        if not is_found:
                            j.path_target = None
                        break
                update.remove(i)
            elif i['code'] == 'CONNECT':
                info = self.world.client.player_info(i['headers']['username'])
                self.players.append(Player(self.world, info))
                update.remove(i)
            elif i['code'] == 'QUIT':
                print 'someone quited'
                for j in self.players:
                    if i['headers']['username'] == j.username:
                        self.players.remove(j)
                        break
                update.remove(i)
            elif i['code'] == 'CHAT':
                for j in self.players:
                    if i['headers']['username'] == j.username:
                        j.msg = i['headers']['message']
                        update.remove(i)
                        break
            elif i['code'] == 'ADD PLAYER':
                is_found = False
                for j in self.players:
                    if j.username == i['headers']['username']:
                        is_found = True
                if not is_found:
                    info = self.world.client.player_info(i['headers']['username'])
                    self.players.append(Player(self.world, data=info))
                self.world.cur_screen.layer_reorder()
                update.remove(i)
            elif i['code'] == 'REMOVE PLAYER':
                for j in self.players:
                    if i['headers']['username'] == j.username:
                        self.players.remove(j)
                        update.remove(i)
                        break
                update.remove(i)
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
                    if j.player.username == i['headers']['addressee'] and j.activity == i['headers']['activity']:
                        if i['headers']['is_accepted'] == 'v':
                            self.activity_requests.remove(j)
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
                                self.xo_menu.stage.pos = [738, -10]
                                self.xo_menu.change_visible(True)
                                self.xo_menu.change_clickable(True)
                        else:
                            j.decline_request()
                        break
                update.remove(i)
            elif i['code'] == 'XO TURN':
                self.xo_menu.play_turn(i['headers']['letter'], int(i['headers']['row']), int(i['headers']['col']))
                winner = self.xo_menu.check_winner()
                if winner:
                    if winner == self.xo_menu.letter:
                        self.message_menu = MessageMenu(self.world, 'You Win!',
                                                        'You defeated ' + self.xo_menu.player.username +
                                                        ' and got the next rewards:', coins=100, xp=200)
                    elif winner == 'XO':
                        self.message_menu = MessageMenu(self.world, 'A Tie!',
                                                        'You tied with ' + self.xo_menu.player.username +
                                                        ' and got the next rewards:', xp=100)
                    else:
                        self.message_menu = MessageMenu(self.world, 'You Lose!',
                                                        'You lost to ' + self.xo_menu.player.username +
                                                        ' and got the next rewards:', coins=-50, xp=50)
                    self.xo_menu = XOMenu(self.world)
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
                self.world.cur_player.update_mission(jenny_missions[1][0][0], False)
                for j in self.players:
                    if i['headers']['user1'] == j.username:
                        for k in i['headers']['items1'].split():
                            for l in j.items:
                                if l.item_id == k:
                                    if l.amount == 1:
                                        j.items.remove(l)
                                    else:
                                        l.amount -= 1
                                    break
                        for k in i['headers']['items2'].split():
                            is_found = False
                            for l in j.items:
                                if l.item_id == k:
                                    is_found = True
                                    l.amount += 1
                            if not is_found:
                                j.items.append(Item(self.world, self.world.client.item_info(k), j.pos, 1, False))
                    elif i['headers']['user2'] == j.username:
                        for k in i['headers']['items2'].split():
                            for l in j.items:
                                if l.item_id == k:
                                    if l.amount == 1:
                                        j.items.remove(l)
                                    else:
                                        l.amount -= 1
                                    break
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
                           list(zip(*self.trade_menu.player_cells)[1]) + self.map_menu.buttons +
                           [self.path, self.chat_box, self.bag_button, self.self_info_menu.x_button,
                            self.player_info_menu.x_button, self.player_info_menu.trade_button,
                            self.player_info_menu.xo_button, self.map_button, self.trade_menu.v_button,
                            self.trade_menu.x_button, self.map_menu, self.xo_menu, self.self_info_menu,
                            self.player_info_menu, self.map_menu.x_button, self.message_menu, self.message_menu.button]
                           + self.players + objects)

    def check_scroll(self, event, objects=None):
        if objects is None:
            objects = []
        Screen.check_scroll(self, event, [self.activity_requests] + objects)

    def draw_screen(self, objects=None):
        for i in self.players:
            i.walk()
            i.check_message()

        if objects is None:
            objects = []
        Screen.draw_screen(self, self.out + [self.path, self.chat_box, self.bag_button, self.self_info_menu,
                                             self.player_info_menu, self.activity_requests, self.trade_menu,
                                             self.map_button, self.map_menu, self.xo_menu, self.message_menu]
                           + self.players + objects)

    def on_click(self, map_object, event):
        if map_object in [self.bag_button, self.self_info_menu.x_button]:
            self.self_info_menu.change_visible()
            self.self_info_menu.change_clickable()
            return
        if map_object is self.map_button:
            self.map_menu.change_visible()
            self.map_menu.change_clickable()
            return
        if map_object in self.map_menu.buttons:
            for i in xrange(len(self.map_menu.buttons)):
                if map_object is self.map_menu.buttons[i]:
                    from Client.screens.Loading import Loading
                    self.world.cur_screen = Loading(self.world, 301, 201 + i)
                    self.world.cur_player.path_target = None
                    self.world.cur_player.update_mission(jon_missions[0][2][0], False)
                    return
        if map_object is self.player_info_menu.x_button:
            self.player_info_menu.change_visible(False)
            self.player_info_menu.change_clickable(False)
            return
        if map_object is self.map_menu.x_button:
            self.map_menu.change_visible(False)
            self.map_menu.change_clickable(False)
            return
        if map_object is self.message_menu.button:
            self.message_menu.change_visible()
            self.message_menu.change_clickable()
            return
        if map_object is self.player_info_menu.trade_button:
            is_found = False
            for i in self.activity_requests:
                if i.activity == 'TRADE' and i.player == self.player_info_menu.player:
                    is_found = True
            if not is_found:
                self.world.client.activity_request('TRADE', self.world.cur_player.username,
                                                   self.player_info_menu.player.username)
                self.activity_requests.append(ActivityRequest(self.world, 'TRADE', self.player_info_menu.player, False))
            return
        if map_object is self.player_info_menu.xo_button:
            if int(self.world.cur_player.coins) < 50 or int(self.player_info_menu.player.coins) < 50:
                self.message_menu = MessageMenu(self.world, "Can't Play!",
                                                'You and your opponent must have at least 50 coins to play.',
                                                is_warning=True)
                return
            is_found = False
            for i in self.activity_requests:
                if i.activity == 'XO' and i.player == self.player_info_menu.player:
                    is_found = True
            if not is_found:
                self.world.client.activity_request('XO', self.world.cur_player.username,
                                                   self.player_info_menu.player.username)
                self.activity_requests.append(ActivityRequest(self.world, 'XO', self.player_info_menu.player, False))
            return
        for i in self.activity_requests:
            for j in i.buttons:
                if map_object is i.buttons[j]:
                    self.world.client.activity_response(i.activity, i.player.username, self.world.cur_player.username,
                                                        j)
                    self.activity_requests.remove(i)
                    if j == 'v':  # Start activity!
                        if i.activity == 'TRADE':
                            self.player_info_menu.change_visible(False)
                            self.player_info_menu.change_clickable(False)
                            self.self_info_menu.change_visible(False)
                            self.self_info_menu.change_clickable(False)
                            self.trade_menu.player = i.player
                            self.trade_menu.change_visible()
                            self.trade_menu.change_clickable()
                        elif i.activity == 'XO':
                            self.world.cur_player.update_mission(charles_missions[0][0][0], False)
                            if self.world.cur_player.check_mission(jon_missions[0][2][0]):
                                Room.charles_mission += 1
                                if Room.charles_mission == 5:
                                    self.world.cur_player.update_mission(jon_missions[0][2][0], False)
                            self.player_info_menu.change_visible(False)
                            self.player_info_menu.change_clickable(False)
                            self.self_info_menu.change_visible(False)
                            self.self_info_menu.change_clickable(False)
                            self.xo_menu.player = i.player
                            self.xo_menu.letter = 'O'
                            self.xo_menu.change_visible()
                            self.xo_menu.change_cells_clickable(False)
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
                    self.world.client.xo_turn(self.xo_menu.player.username, self.xo_menu.letter, i, j)
                    winner = self.xo_menu.check_winner()
                    if winner:
                        if winner == self.xo_menu.letter:
                            self.world.cur_player.update_mission(charles_missions[0][1][0], False)
                            self.message_menu = MessageMenu(self.world, 'You Win!', 'You defeated ' +
                                                            self.xo_menu.player.username + ' and got the next rewards:',
                                                            coins=50, xp=200)
                        elif winner == 'XO':
                            self.message_menu = MessageMenu(self.world, 'A Tie!',
                                                            'You tied with ' + self.xo_menu.player.username +
                                                            ' and got the next rewards:', xp=100)
                        else:
                            self.message_menu = MessageMenu(self.world, 'You Lose!',
                                                            'You lost to ' + self.xo_menu.player.username +
                                                            ' and got the next rewards:', coins=-50, xp=50)
                        self.xo_menu = XOMenu(self.world)

    def on_type(self, map_object, event):
        raise NotImplementedError

    def on_scroll(self, map_object, event):
        if map_object is self.activity_requests:
            self.activity_requests.scroll(event.button == 4)

    def layer_reorder(self):
        raise NotImplementedError
