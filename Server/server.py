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
        # Initialize
        cred = credentials.Certificate(r'C:\Users\USER\Downloads\cyberproject-ec385-firebase-adminsdk-sxzt7-5b7e34d38f.json')
        firebase_admin.initialize_app(cred, {'databaseURL': 'https://cyberproject-ec385.firebaseio.com',
                                             'storageBucket': 'cyberproject-ec385.appspot.com'})
        self.bucket = storage.bucket()

        self.socket = socket.socket()
        self.socket.bind(SERVER_ADDRESS)
        self.socket.listen(5)
        self.client_sockets = []
        self.waiting_data = []

        while True:
            sockets = []
            for i in self.client_sockets:
                if 'socket' in i:
                    sockets.append(i['socket'])
            rlist, wlist, xlist = select.select(sockets + [self.socket], sockets, [])
            for i in rlist:
                if i is self.socket:
                    new_socket, address = self.socket.accept()
                    self.client_sockets.append({'socket': new_socket, 'username': None, 'room_id': 0})
                else:
                    self.receive_message(i)

            for client, msg in self.waiting_data:
                if client in wlist:
                    self.send_message(client, msg['code'], msg['headers'], msg['data'])
                    self.waiting_data.remove([client, msg])

    def add_message(self, client_socket, code, headers, data=''):
        self.waiting_data.append([client_socket, {'code': code, 'headers': headers, 'data': data}])

    def send_message(self, client_socket, code, headers, data=''):
        # Protocol
        headers['length'] = len(data)
        response = Server.message_format(code, headers, data)
        while response != '':
            try:
                client_socket.send(response[:KB])
            except socket.error:
                print 'Error: No client communication!'
                for i in self.client_sockets:
                    if i['socket'] == client_socket:
                        print 'QUIT', i['username']
                        ref = db.reference('rooms/' + i['room_id'] + '/players/' + i['username'])
                        ref.delete()
                        for j in self.client_sockets:
                            self.add_message(j, 'QUIT', {'username': i['username']})
                        self.client_sockets.remove(i)
                        break
                return
            response = response[KB:]

    def receive_message(self, client_socket):
        try:
            msg = client_socket.recv(KB)
        except (socket.error, socket.timeout):
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
                data += client_socket.recv(KB)
            except socket.error:
                print 'Error: No client communication!'
                for i in self.client_sockets:
                    if i['socket'] == self.client_sockets:  # TODO: Remove player
                        ref = db.reference('rooms/' + i['room_id'] + '/players/' + i['username'])
                        ref.delete()
                        for j in self.client_sockets:
                            self.add_message(j, 'QUIT', {'username': i['username']})
                        self.client_sockets.remove(i)
                        break
                return
        if command == 'STORAGE':
            blob = self.bucket.get_blob(headers['item'])
            self.add_message(client_socket, 'OK', {'time-created': blob.time_created, 'command': command}, blob.download_as_string())
        elif command == 'POS':
            ref = db.reference('users/' + headers['username'])
            pos = headers['pos'].split(' ')
            ref.update({'pos': [int(pos[0]), int(pos[1])]})
            for i in self.client_sockets:
                if i['socket'] == client_socket:
                    self.add_message(client_socket, 'OK', {'command': command})
                else:
                    self.add_message(i['socket'], 'POS', {'username': headers['username'], 'command': command}, headers['pos'])
        elif command == 'CREATE PLAYER':
            ref = db.reference('users/')
            print headers['username']
            ref.child(headers['username']).set({
                'is_male': bool(headers['is_male']),
                'items': headers['items'][1:-1].split(', '),
                'level': int(headers['level']),
                'join_date': headers['join_date'],
                'is_admin': bool(headers['is_admin']),
                'room_id': int(headers['room_id']),
                'pos': map(lambda p: int(p), headers['pos'][1:-1].split(', '))
            })
            self.add_message(client_socket, 'OK', {'command': command})
        elif command == 'ADD PLAYER':
            room_id = db.reference('users/' + headers['username'] + '/room_id').get()
            db.reference('rooms/' + str(room_id) + '/players').delete()

            db.reference('users/' + headers['username'] + '/room_id').set(int(headers['room_id']))

            ref = db.reference('rooms/' + headers['room_id'] + '/players')
            ref.child(headers['username']).set(True)
            for i in self.client_sockets:
                if i['socket'] == client_socket:
                    self.add_message(client_socket, 'OK', {'command': command})
                else:
                    self.add_message(i['socket'], 'ADD PLAYER', {'username': headers['username'], 'room_id': headers['room_id'], 'command': command})
        elif command == 'PLAYER INFO':
            ref = db.reference('users/' + headers['username']).get()
            info = {'username': headers['username']}
            for key, value in ref.iteritems():
                if type(key) is unicode:
                    key = str(key)
                if type(value) is unicode:
                    value = str(value)
                info[key] = value
            self.add_message(client_socket, 'OK', {'command': command}, str(info))
        elif command == 'ROOM PLAYERS':
            ref = db.reference('rooms/' + headers['room_id'] + '/players').get()
            if ref:
                self.add_message(client_socket, 'OK', {'command': command}, ' '.join(ref))
            else:
                self.add_message(client_socket, 'OK', {'command': command})
        elif command == 'CONNECT':
            room_id = db.reference('users/' + headers['username'] + '/room_id').get()
            ref = db.reference('rooms/' + str(room_id) + '/players')
            ref.child(headers['username']).set(True)
            self.add_socket_details(client_socket, headers['username'], str(room_id))
            for i in self.client_sockets:
                if i['socket'] == client_socket:
                    self.add_message(client_socket, 'OK', {'command': command})
                else:
                    self.add_message(i['socket'], 'ADD PLAYER', {'username': headers['username'], 'room_id': room_id, 'command': command})
        elif command == 'QUIT':
            print 'QUITTT'
            ref = db.reference('rooms/' + headers['room_id'] + '/players/' + headers['username'])
            ref.delete()
            for i in self.client_sockets:
                self.add_message(i, 'QUIT', {'username': headers['username'], 'command': command})
            self.add_message(client_socket, 'OK', {'command': command})
        elif command == 'CHAT':
            for i in self.client_sockets:
                if i['socket'] == client_socket:
                    self.add_message(client_socket, 'OK', {'command': command})
                else:
                    self.add_message(i['socket'], 'CHAT', {'username': headers['username'], 'message': headers['message'], 'command': command})

    def add_socket_details(self, client_socket, username, room_id):
        for i in self.client_sockets:
            if i['socket'] == client_socket:
                i['username'] = username
                i['room_id'] = room_id
                break

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