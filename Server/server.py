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
        cred = credentials.Certificate(r'C:\Users\USER\Downloads\cyberproject-ec385-firebase-adminsdk-sxzt7-5b7e34d38f.json')
        firebase_admin.initialize_app(cred, {'databaseURL': 'https://cyberproject-ec385.firebaseio.com',
                                             'storageBucket': 'cyberproject-ec385.appspot.com'})
        self.bucket = storage.bucket()

        self.socket = socket.socket()
        self.socket.bind(SERVER_ADDRESS)
        self.socket.listen(5)

        while True:
            client_socket, address = self.socket.accept()
            self.wait_for_command(client_socket)

    def send_message(self, client_socket, msg):
        client_socket.send(msg)

    def wait_for_command(self, client_socket):
        while True:
            try:
                msg = client_socket.recv(KB)
            except (socket.error, socket.timeout):
                break

            parts = msg.split('\r\n')
            command, param = parts[0], parts[1:]
            if command == 'STORAGE':
                blob = self.bucket.blob(param[0])
                answer = blob.download_as_string() + '\r\n' + blob.time_created
                self.send_message(client_socket, answer)


def main():
    server = Server()

if __name__ == '__main__':
    main()