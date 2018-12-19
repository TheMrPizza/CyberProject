from mechanics.World import World
from screens.Beach import Beach
from mechanics.Player import Player
from screens import Login

import os
import time
import socket

SERVER_ADDRESS = ('192.168.10.147', 1943)
KB = 1024


class Client:
    def __init__(self):
        self.socket = socket.socket()
        self.socket.connect(SERVER_ADDRESS)

    def send_message(self, msg):
        self.socket.send(msg)
        return self.socket.recv(KB)

    def get_from_storage(self, item):
        file_path = os.path.dirname(os.path.abspath(__file__)) + '/' + item
        answer = self.send_message('STORAGE\r\n' + item)
        param = answer.split('\r\n')

        if os.path.exists(file_path):
            if os.path.getctime(file_path) < time.mktime(param[1].timetuple()):
                # File was changed! Update
                item_file = open(file_path, 'w')
                item_file.write(param[0])
                item_file.close()
        else:
            # File doesn't exist! Download
            item_file = open(file_path, 'w')
            item_file.write(param[0])
            item_file.close()


def main():
    client = Client()
    path = os.path.dirname(os.path.abspath(__file__))
    world = World(path, client)
    # world.cur_screen = Login(world)
    b = Beach(world)
    b.players = [Player(world, 'guy1guy1', True, [], 15, '23.11.18', True, 201, [200, 300])]
    world.cur_screen = b


if __name__ == '__main__':
    main()

