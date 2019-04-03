import firebase_admin
from firebase_admin import credentials
from firebase_admin import storage
from firebase_admin import db

import socket
import select

SERVER_ADDRESS = ('0.0.0.0', 1943)
KB = 1024


class Server(object):
    def __init__(self):
        # Initialize Firebase database and storage
        cred = credentials.Certificate(r'C:\Users\USER\Downloads\cyberproject-ec385-firebase-adminsdk-sxzt7-5b7e34d38f.json')
        firebase_admin.initialize_app(cred, {'databaseURL': 'https://cyberproject-ec385.firebaseio.com',
                                             'storageBucket': 'cyberproject-ec385.appspot.com'})
        self.bucket = storage.bucket()

        # Initialize the server socket
        self.socket = socket.socket()
        self.socket.bind(SERVER_ADDRESS)
        self.socket.listen(5)

        self.client_players = []  # The client socket and client's player username and room id
        self.waiting_data = []  # Data to send to clients

        while True:
            sockets = []
            for i in self.client_players:
                if 'socket' in i:
                    sockets.append(i['socket'])
            rlist, wlist, xlist = select.select(sockets + [self.socket], sockets, [])
            for i in rlist:  # Reading messages
                if i is self.socket:  # New client, adding to client players
                    new_socket, address = self.socket.accept()
                    self.client_players.append({'socket': new_socket, 'username': '', 'room_id': '0'})
                else:  # Known client, receiving message
                    for j in self.client_players:
                        if i == j['socket']:
                            self.receive_message(j)
                            break

            for client_player, msg in self.waiting_data:  # Sending messages
                if client_player['socket'] in wlist:
                    self.send_message(client_player, msg['code'], msg['headers'], msg['data'])
                    self.waiting_data.remove([client_player, msg])

    def add_message(self, client_player, code, headers, data=''):
        self.waiting_data.append([client_player, {'code': code, 'headers': headers, 'data': data}])

    def send_message(self, client_player, code, headers, data=''):
        # Protocol
        headers['length'] = len(data)
        response = Server.message_format(code, headers, data)
        while response != '':
            try:
                client_player['socket'].send(response[:KB])
            except socket.error:
                self.quit_socket(client_player)
                return
            response = response[KB:]

    def receive_message(self, client_player):
        try:
            msg = client_player['socket'].recv(KB)
        except (socket.error, socket.timeout):
            self.quit_socket(client_player)
            return
        if msg == '':
            return
        lines = msg.split('\r\n')
        command = lines[0]
        headers = {}
        data = ''
        for i in xrange(1, len(lines)-1):
            if lines[i] == '':
                data = ''.join(lines[i + 1:])
                break
            parts = lines[i].split(': ')
            headers[parts[0]] = parts[1]

        while int(headers['length']) != len(data):
            try:
                data += client_player['socket'].recv(KB)
            except socket.error:
                self.quit_socket(client_player)
                return

        if command == 'STORAGE':
            blob = self.bucket.get_blob(headers['item'])
            self.add_message(client_player, 'OK', {'time-created': blob.time_created, 'command': command},
                             blob.download_as_string())
        elif command == 'POS':
            ref = db.reference('users/' + headers['username'])
            pos = headers['pos'].split(' ')
            ref.update({'pos': [int(pos[0]), int(pos[1])]})
            for i in self.client_players:
                if i == client_player:
                    self.add_message(client_player, 'OK', {'command': command})
                elif i['room_id'] == client_player['room_id']:
                    self.add_message(i, 'POS', {'username': headers['username'], 'command': command},
                                     headers['pos'])
        elif command == 'CREATE PLAYER':
            ref = db.reference('users/')
            print headers['username']
            ref.child(headers['username']).set({
                'body': headers['body'],
                'is_male': bool(headers['is_male']),
                'items': headers['items'][1:-1].split(', '),
                'level': int(headers['level']),
                'join_date': headers['join_date'],
                'is_admin': bool(headers['is_admin']),
                'room_id': int(headers['room_id']),
                'pos': map(lambda p: int(p), headers['pos'][1:-1].split(', '))
            })
            self.add_message(client_player, 'OK', {'command': command})
        elif command == 'ADD PLAYER':
            # Delete player from the old room
            room_id = db.reference('users/' + headers['username'] + '/room_id').get()
            db.reference('rooms/' + str(room_id) + '/players').delete()

            # Add player to the new room
            db.reference('users/' + headers['username'] + '/room_id').set(int(headers['room_id']))
            ref = db.reference('rooms/' + headers['room_id'] + '/players')
            ref.child(headers['username']).set(True)

            for i in self.client_players:
                if i is client_player:  # The player, send him OK
                    i['room_id'] = headers['room_id']
                    self.add_message(client_player, 'OK', {'command': command})
                elif int(i['room_id']) == room_id:  # A player in the old room, say goodbye
                    self.add_message(i, 'REMOVE PLAYER', {'username': headers['username'],
                                                                    'room_id': headers['room_id'], 'command': command})
                elif i['room_id'] == headers['room_id']:  # A player in the new room, say hello
                    self.add_message(i, 'ADD PLAYER', {'username': headers['username'],
                                                                 'room_id': headers['room_id'], 'command': command})
        elif command == 'PLAYER INFO':
            ref = db.reference('users/' + headers['username']).get()
            info = {'username': headers['username']}
            for key, value in ref.iteritems():
                if type(key) is unicode:
                    key = str(key)
                if type(value) is unicode:
                    value = str(value)
                info[key] = value
            self.add_message(client_player, 'OK', {'command': command}, str(info))
        elif command == 'ITEM INFO':
            ref = db.reference('items/' + headers['item_id']).get()
            info = {'item_id': headers['item_id']}
            for key, value in ref.iteritems():
                if type(key) is unicode:
                    key = str(key)
                if type(value) is unicode:
                    value = str(value)
                info[key] = value
            self.add_message(client_player, 'OK', {'command': command}, str(info))
        elif command == 'CHANGE ITEM':
            ref = db.reference('users/' + headers['username'] + '/items/' + headers['item_id'] + '/is_used')
            ref.set(not ref.get())
            for i in self.client_players:
                if i is client_player:
                    self.add_message(client_player, 'OK', {'command': command})
                elif i['room_id'] == client_player['room_id']:
                    self.add_message(i, 'CHANGE ITEM', {'username': headers['username'], 'item_id': headers['item_id'],
                                                        'command': command})
        elif command == 'ROOM PLAYERS':
            ref = db.reference('rooms/' + headers['room_id'] + '/players').get()
            if ref:
                self.add_message(client_player, 'OK', {'command': command}, ' '.join(ref))
            else:
                self.add_message(client_player, 'OK', {'command': command})
        elif command == 'CONNECT':
            room_id = db.reference('users/' + headers['username'] + '/room_id').get()
            ref = db.reference('rooms/' + str(room_id) + '/players')
            ref.child(headers['username']).set(True)
            self.add_socket_details(client_player, headers['username'], str(room_id))
            for i in self.client_players:
                if i is client_player:
                    self.add_message(client_player, 'OK', {'command': command})
                elif int(i['room_id']) == room_id:
                    self.add_message(i, 'ADD PLAYER', {'username': headers['username'],
                                                                 'room_id': room_id, 'command': command})
        elif command == 'QUIT':
            print 'QUITTT'
            ref = db.reference('rooms/' + headers['room_id'] + '/players/' + headers['username'])
            ref.delete()
            for i in self.client_players:
                self.add_message(i, 'QUIT', {'username': headers['username'], 'command': command})
            self.add_message(client_player, 'OK', {'command': command})
        elif command == 'CHAT':
            for i in self.client_players:
                if i is client_player:
                    self.add_message(client_player, 'OK', {'command': command})
                else:
                    self.add_message(i, 'CHAT', {'username': headers['username'],
                                                           'message': headers['message'], 'command': command})

    def add_socket_details(self, client_player, username, room_id):
        client_player['username'] = username
        client_player['room_id'] = room_id

    def quit_socket(self, client_player):
        print 'Error: No client communication!'
        print 'QUIT', client_player['username']
        ref = db.reference('rooms/' + client_player['room_id'] + '/players/' + client_player['username'])
        ref.delete()
        for i in self.client_players:
            self.add_message(i, 'QUIT', {'username': client_player['username']})
        self.client_players.remove(client_player)

    @staticmethod
    def message_format(command, headers, data):
        msg = command + '\r\n'
        for i in headers:
            msg += str(i) + ': ' + str(headers[i]) + '\r\n'
        msg += '\r\n' + data
        return msg


def main():
    server = Server()


if __name__ == '__main__':
    main()
