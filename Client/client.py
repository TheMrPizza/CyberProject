from mechanics.World import World
from screens.Beach import Beach
from mechanics.Player import Player
from screens.Login import Login

import os
import time
from datetime import datetime
import socket
import ast

SERVER_ADDRESS = ('127.0.0.1', 1943)
KB = 1024


class Client:
    def __init__(self):
        self.FILE_PATH = os.path.dirname(os.path.abspath(__file__)) + '/'
        self.socket = socket.socket()
        self.socket.connect(SERVER_ADDRESS)

    def send_message(self, command, headers, data=''):
        # Protocol
        headers['length'] = len(data)
        request = Client.message_format(command, headers, data)
        while request != '':
            self.socket.send(request[:KB])
            request = request[KB:]

        code, headers, data = self.receive_message()
        if code == 'OK':
            return headers, data

    def receive_message(self):
        msg = self.socket.recv(KB)
        lines = msg.split('\r\n')
        code = lines[0]
        headers = {}
        data = ''
        for i in xrange(1, len(lines) - 1):
            if lines[i] == '':
                data = '\r\n'.join(lines[i + 1:])
                break
            parts = lines[i].split(': ')
            headers[parts[0]] = parts[1]

        while int(headers['length']) != len(data):
            data += self.socket.recv(KB)
        return code, headers, data

    @staticmethod
    def message_format(command, headers, data):
        msg = command + '\r\n'
        for i in headers:
            msg += str(i) + ': ' + str(headers[i]) + '\r\n'
        msg += '\r\n' + data
        return msg

    def get_from_storage(self, item):
        headers, data = self.send_message('STORAGE', {'item': item})
        item_path = self.FILE_PATH + item
        if os.path.exists(item_path):
            if os.path.getctime(item_path) < time.mktime(datetime.strptime(headers['time-created'][:-6], '%Y-%m-%d %H:%M:%S.%f').timetuple()):
                # File was changed! Update
                item_file = open(item_path, 'wb')
                item_file.write(data)
                item_file.close()
        else:
            # File doesn't exist! Download
            item_file = open(item_path, 'wb')
            item_file.write(data)
            item_file.close()

    def create_player(self, player):
        self.send_message('CREATE PLAYER', {'username': player.username, 'is_male': player.is_male,
                                            'items': player.items, 'level': player.level, 'join_date': player.join_date,
                                            'is_admin': player.is_admin, 'room_id': player.room_id, 'pos': player.pos})
        self.add_player(player.room_id, player.username)

    def add_player(self, room_id, username):
        self.send_message('ADD PLAYER', {'room_id': room_id, 'username': username})

    def player_info(self, username):
        headers, data = self.send_message('PLAYER INFO', {'username': username})
        return ast.literal_eval(data)

    def find_players(self, room_id):
        headers, data = self.send_message('ROOM PLAYERS', {'room_id': room_id})
        return data.split(' ')

    def update_player_pos(self, username, pos):
        self.send_message('POS', {'username': username, 'pos': str(pos[0]) + ' ' + str(pos[1])})


def main():
    client = Client()
    world = World(client.FILE_PATH, client)
    world.cur_screen = Login(world)
    #b = Beach(world)
    #b.players = [Player(world, 'guy2guy2', True, [], 15, '23.11.18', True, 201, [400, 200])]
    #world.cur_screen = b


if __name__ == '__main__':
    main()

