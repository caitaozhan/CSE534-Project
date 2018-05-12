from tcprelay import TCPRelay
import socket
import threading
from utility import read_config
import sys


class Client:
    def __init__(self, config):
        self.local_addr = config["local_addr"]
        config["local_port"] = int(config["local_port"])
        self.local_port = config["local_port"]

        self.local_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.local_socket.bind((self.local_addr, self.local_port))
        self.local_socket.listen(1024)
        print('Listening at {}:{}'.format(self.local_addr, self.local_port))

        self.remote_addr = config["server_addr"]
        config["server_port"] = int(config["server_port"])
        self.remote_port = config["server_port"]

        self.config = config
        self.config["is_client"] = True

    def new_tcprelay(self, local_sock):
        tcp = TCPRelay(self.config, local_sock)
        tcp.run()

    def loop(self):
        while True:
            local_sock, local_addr = self.local_socket.accept()
            print("Receive local data from {}".format(local_addr))
            t = threading.Thread(target=self.new_tcprelay, args=[local_sock])
            t.start()


def main():
    try:
        path = sys.argv[1]
    except:
        path = "client_config.json"
    config = read_config(path)
    client = Client(config)
    client.loop()


if __name__ == '__main__':
    main()
