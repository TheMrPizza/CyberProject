from MapObject import MapObject
from Client.mechanics.TextBox import TextBox
from Client.mechanics.ImageButton import ImageButton
from Client.mechanics.InfoMenu import InfoMenu
from Player import Player
from Client.mechanics.AStar.Search import search_path
from Screen import Screen


class Room(Screen):
    def __init__(self, world, room_id, bg_image, path, out):
        Screen.__init__(self, world, room_id, bg_image)
        self.path = MapObject(self.world, [0, 0], image=path, size=world.SIZE, is_transparent=True)
        self.out = out
        self.chat_box = TextBox(self.world, [None, 540], 720, middle=self.bg_image)
        self.bag_button = ImageButton(self.world, [900, 540], 'images/test_text_box.9.png', [50, 50], 'images/bag.png')
        self.bag = MapObject(self.world, [600, 540], image='images/bag.png')
        self.info_menu = InfoMenu(world)

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

    def check_event(self, event, objects=None):
        if objects is None:
            objects = []
        Screen.check_event(self, event, self.out + list(zip(*self.info_menu.cells)[1]) + [self.path, self.bag_button] + self.players + objects)

    def draw_screen(self, objects=None):
        for i in self.players:
            i.walk()
            i.check_message()

        if objects is None:
            objects = []
        Screen.draw_screen(self, self.out + [self.path, self.bag_button, self.info_menu] + self.players + objects)

    def on_click(self, map_object, event):
        if map_object is self.bag_button:
            self.info_menu.change_focus()
        for i in self.info_menu.cells:
            if map_object is i[1] and map_object.front:
                for j in self.world.cur_player.items:
                    if j.item_id == i[0]:
                        self.world.cur_player.change_item(j)
                        break
                break

    def on_type(self, map_object, event):
        raise NotImplementedError
