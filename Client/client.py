from mechanics.World import World
from screens.Login import Login

import os
import time
from datetime import datetime
import socket
import ast
import threading
import sys

SERVER_ADDRESS = ('127.0.0.1', 1943)
KB = 1024


class Client(object):
    def __init__(self):
        self.FILE_PATH = os.path.dirname(os.path.abspath(__file__)) + '/'
        self.socket = socket.socket()
        try:
            self.socket.connect(SERVER_ADDRESS)
        except socket.error:
            print 'Error: No server communication!'
            sys.exit()
        self.updates = []
        self.thread = threading.Thread(target=self.receive_message)
        self.thread.start()

    def send_message(self, command, headers, data=''):
        # Protocol
        print command, headers, data
        headers['length'] = len(data)
        request = Client.message_format(command, headers, data)
        while request != '':
            try:
                self.socket.send(request[:KB])
            except socket.error:
                print 'Error: No server communication!'
                sys.exit()
            request = request[KB:]

        while True:
            for i in self.updates:
                if i['headers']['command'] == command:
                    code, headers, data = i['code'], i['headers'], i['data']
                    self.updates.remove(i)
                    if code == 'OK':
                        return headers, data

    def receive_message(self):
        while True:
            try:
                msg = self.socket.recv(KB)
            except socket.error:
                print 'Error: No server communication!'
                sys.exit()
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
                try:
                    data += self.socket.recv(KB)
                except socket.error:
                    print 'Error: No server communication!'
                    sys.exit()

            self.updates.append({'code': code, 'headers': headers, 'data': data})

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
            if time.time() - os.path.getctime(item_path) > 60*60*24:  # Check if the file updated in the last 24 hours
                # The file is already updated
                return
            if os.path.getctime(item_path) < time.mktime(datetime.strptime(headers['time-created'][:-6],
                                                                           '%Y-%m-%d %H:%M:%S.%f').timetuple()):
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
        print ast.literal_eval(data)
        return ast.literal_eval(data)

    def item_info(self, item_id):
        headers, data = self.send_message('ITEM INFO', {'item_id': item_id})
        print ast.literal_eval(data)
        return ast.literal_eval(data)

    def find_players(self, room_id):
        headers, data = self.send_message('ROOM PLAYERS', {'room_id': room_id})
        if data:
            return data.split(' ')
        return []

    def update_player_pos(self, username, pos):
        self.send_message('POS', {'username': username, 'pos': str(pos[0]) + ' ' + str(pos[1])})

    def connect(self, username):
        self.send_message('CONNECT', {'username': username})

    def quit(self, username, room_id):
        self.send_message('QUIT', {'username': username, 'room_id': room_id})

    def chat(self, username, message):
        self.send_message('CHAT', {'username': username, 'message': message})


def main():
    client = Client()
    world = World(client.FILE_PATH, client)
    world.cur_screen = Login(world)

if __name__ == '__main__':
    main()
