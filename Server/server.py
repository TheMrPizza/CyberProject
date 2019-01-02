import firebase_admin
from firebase_admin import credentials
from firebase_admin import storage
from firebase_admin import db

import socket
import select

SERVER_ADDRESS = ('0.0.0.0', 1943)
KB = 1024


class Server:
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
            rlist, wlist, xlist = select.select(self.client_sockets + [self.socket], self.client_sockets, [])
            for i in rlist:
                if i is self.socket:
                    new_socket, address = self.socket.accept()
                    self.client_sockets.append(new_socket)
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
        headers['Length'] = len(data)
        response = Server.message_format(code, headers, data)
        while response != '':
            client_socket.send(response[:KB])
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

        while int(headers['Length']) != len(data):
            data += client_socket.recv(KB)

        if command == 'STORAGE':
            blob = self.bucket.get_blob(headers['Item'])
            self.add_message(client_socket, 'OK', {'Time-created': blob.time_created}, blob.download_as_string())
        elif command == 'POS':
            ref = db.reference('users/' + headers['Username'])
            pos = headers['Pos'].split(' ')
            ref.update({'pos': [int(pos[0]), int(pos[1])]})
            self.add_message(client_socket, 'OK', {})

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