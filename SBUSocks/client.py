import argparse
import threading
import socket
from cipher import Cipher
import time


class Client:
    BUF_SIZE = 32 * 1024

    def __init__(self, config):
        self.local_addr = config["local_addr"]
        self.local_port = config["local_port"]

        self.local_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.local_socket.bind((self.local_addr,self.local_port))
        self.local_socket.listen(1024)
        print('Listening at {}:{}'.format(self.local_addr, self.local_port))


        self.remote_addr = config["server_addr"]
        self.remote_port = config["server_port"]
        self.remote_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        

        self.cipher = Cipher()

        self.socks = []


    def connect_server(self):
        while True:
            try:
                self.server_socket.connect((self.server_addr,self.server_port))
            except:
                print("Server Offline!")
                time.sleep(1)
        

    def receive_local(self):
        print('Accept from local port')
        while True:
            data = sock.recv(self.BUF_SIZE)
            data = self.cipher.encrypt(data)
            if not data:
                break
            try:
                self.server_socket.send(data)
            except OSError:
                self.connect_server()
                self.server_socket.send(data)

        sock.close()
        print('Connection from %s:%s closed.' % addr)

    def send_server(self):
        print('Send to server')


    def send_local(self, sock, addr):
        print('Accept new connection from %s:%s...' % addr)

    def receive_server(self, sock, addr):
        while True:
            data = sock.recv(self.BUF_SIZE)
            data = self.cipher.decrypt(data)
            if not data:
                break


    def loop(self):
        while True:

            local_sock, local_addr = self.local_socket.accept()
            forward = threading.Thread(target=self.handle_local, args=[local_sock,local_addr])
            server_sock, server_addr = self.server_socket.accept()
            except OSError:
                connect_server()
                server_sock, server_addr = self.server_socket.accept()

            backward = threading.Thread(target=self.handle_server, args=[server_sock,server_addr])
            forward.start()



def main():
    config = {"local_addr": "127.0.0.1",
              "local_port": 1080,
              "server_addr": "127.0.0.1",
              "server_port": 1234}
    client = Client(config)
    client.run()

    
    connection_handler(sock, addr)


    


if __name__ == '__main__':
    main()