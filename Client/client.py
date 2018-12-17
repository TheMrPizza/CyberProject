from mechanics.World import World
from screens.Beach import Beach
from mechanics.Player import Player
from screens import Login

import os
import time

import firebase_admin
from firebase_admin import credentials
from firebase_admin import storage


def main():
    # Initialize
    cred = credentials.Certificate(r'JSON-FILE-PATH')
    firebase_admin.initialize_app(cred, {'databaseURL': 'https://cyberproject-ec385.firebaseio.com',
                                         'storageBucket': 'cyberproject-ec385.appspot.com'})

    # Storage
    path = os.path.dirname(os.path.abspath(__file__))
    bucket = storage.bucket()
    for i in bucket.list_blobs():
        if i.name.endswith('.png'):
            file_path = path + '/' + i.name
            if os.path.exists(file_path):
                if os.path.getctime(path + '/' + i.name) < time.mktime(i.time_created.timetuple()):
                    # File was changed! Update
                    i.download_to_filename(file_path)
            else:
                # File doesn't exist! Download
                i.download_to_filename(file_path)

    world = World(path + '/images/')
    # world.cur_screen = Login(world)
    b = Beach(world)
    b.players = [Player(world, 'guy1guy1', True, [], 15, '23.11.18', True, 201, [200, 300])]
    world.cur_screen = b


if __name__ == '__main__':
    main()

