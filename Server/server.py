import firebase_admin
from firebase_admin import credentials
from firebase_admin import storage
from firebase_admin import db

import socket

SERVER_ADDRESS = ('0.0.0.0', 1943)
KB = 1024


class Server:
    def __init__(self):
        # Initialize
        cred = credentials.Certificate(r'C:\Users\Guy\Downloads\cyberproject-ec385-firebase-adminsdk-sxzt7-5b7e34d38f.json')
        firebase_admin.initialize_app(cred, {'databaseURL': 'https://cyberproject-ec385.firebaseio.com',
                                             'storageBucket': 'cyberproject-ec385.appspot.com'})
        self.bucket = storage.bucket()

        self.socket = socket.socket()
        self.socket.bind(SERVER_ADDRESS)
        self.socket.listen(5)

        while True:
            client_socket, address = self.socket.accept()
            self.receive_message(client_socket)

    def send_message(self, client_socket, code, headers, data=''):
        # Protocol
        headers['Length'] = len(data)
        response = Server.message_format(code, headers, data)
        while response != '':
            client_socket.send(response[:KB])
            response = response[KB:]

    def receive_message(self, client_socket):
        while True:
            try:
                msg = client_socket.recv(KB)
            except (socket.error, socket.timeout):
                break
            if msg == '':
                break
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
                self.send_message(client_socket, 'OK', {'Time-created': blob.time_created}, blob.download_as_string())
            elif command == 'POS':
                ref = db.reference('users/' + headers['Username'])
                pos = headers['Pos'].split(' ')
                ref.update({'pos': [int(pos[0]), int(pos[1])]})
                self.send_message(client_socket, 'OK', {})

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