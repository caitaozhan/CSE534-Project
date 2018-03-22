from tcprelay import TCPRelay
import socket
import threading
from cipher import Cipher
        
class Server:

    def __init__(self, config):
        self.local_addr = config["local_addr"]
        self.local_port = config["local_port"]

        self.local_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.local_socket.bind((self.local_addr,self.local_port))
        self.local_socket.listen(1024)
        print('Listening at {}:{}'.format(self.local_addr, self.local_port))

    
        self.cipher = Cipher()
        self.config = config
        self.config["is_client"] = False

    def new_tcprelay(self, local_sock):
        tcp = TCPRelay(self.config, local_sock)
        tcp.run()
        

    def loop(self):
        while True:
            local_sock, local_addr = self.local_socket.accept()
            t = threading.Thread(target = self.new_tcprelay, args=[local_sock])
            t.start()
            
def main():
    config = {"local_addr": "0.0.0.0",
              "local_port": 9000}
    server = Server(config)
    server.loop()


    
if __name__ == '__main__':
    main()