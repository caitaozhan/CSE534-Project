import argparse
import threading
import socket

class Server:
    BUF_SIZE = 32 * 1024

    def __init__(self, config):
        self.local_addr = config["local_addr"]
        self.local_port = config["local_port"]
        self.local_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.local_socket.bind((self.local_addr,self.local_port))
        self.local_socket.listen(1024)
        print('Listening at {}:{}'.format(self.local_addr, self.local_port))


    def connection_handler(self, sock, addr):
        print('Accept new connection from %s:%s...' % addr)
        while True:
            data = sock.recv(self.BUF_SIZE)
            if not data:
                break
            print(data)
        sock.close()
        print('Connection from %s:%s closed.' % addr)

    def run(self):
        while True:
            sock, addr = self.local_socket.accept()
            t = threading.Thread(target=self.connection_handler, args=[sock, addr])
            t.start()






def main():
    config = {"local_addr": "127.0.0.1",
              "local_port": 1234}
    server = Server(config)
    server.run()

    
    connection_handler(sock, addr)


    


if __name__ == '__main__':
    main()