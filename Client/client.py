from mechanics.World import World
from screens.Beach import Beach
from mechanics.Player import Player
from screens import Login

import os
import time
from datetime import datetime
import socket

SERVER_ADDRESS = ('127.0.0.1', 1943)
KB = 1024


class Client:
    def __init__(self):
        self.FILE_PATH = os.path.dirname(os.path.abspath(__file__)) + '/'
        self.socket = socket.socket()
        self.socket.connect(SERVER_ADDRESS)

    def send_message(self, command, headers, data=''):
        # Protocol
        headers['Length'] = len(data)
        request = Client.message_format(command, headers, data)
        while request != '':
            self.socket.send(request[:KB])
            request = request[KB:]

        code, headers, data = self.receive_message()
        if code == 'OK':
            if command == 'STORAGE':
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

        while int(headers['Length']) != len(data):
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
        param, data = self.send_message('STORAGE', {'Item': item})
        item_path = self.FILE_PATH + item
        if os.path.exists(item_path):
            if os.path.getctime(item_path) < time.mktime(datetime.strptime(param['Time-created'][:-6], '%Y-%m-%d %H:%M:%S.%f').timetuple()):
                # File was changed! Update
                item_file = open(item_path, 'wb')
                item_file.write(data)
                item_file.close()
        else:
            # File doesn't exist! Download
            item_file = open(item_path, 'wb')
            item_file.write(data)
            item_file.close()

    def find_players(self, room_id):
        # Add self.send_message('ROOM PLAYERS')
        pass

    def update_player_pos(self, username, pos):
        self.send_message('POS', {'Username': username, 'Pos': str(pos[0]) + ' ' + str(pos[1])})


def main():
    client = Client()
    world = World(client.FILE_PATH, client)
    # world.cur_screen = Login(world)
    b = Beach(world)
    b.players = [Player(world, 'guy1guy1', True, [], 15, '23.11.18', True, 201, [200, 300])]
    world.cur_screen = b


if __name__ == '__main__':
    main()

