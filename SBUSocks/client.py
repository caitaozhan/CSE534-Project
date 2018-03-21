import argparse
import threading
import socket
from cipher import Cipher
import select
import sys
import pdb


class InitFailure(Exception):
    pass

class RemoteClose(Exception):
    pass

class TimeOut(Exception):
    pass

class ClientTCPRelay:
    TIMEOUT = 5
    BUF_SIZE = 32 * 1024
    STAGE_STREAM = 1
    STAGE_INIT = 0
    def __init__(self, config, local_sock):
        self.local_addr = config["local_addr"]
        self.local_port = config["local_port"]
        self.remote_addr = config["server_addr"]
        self.remote_port = config["server_port"]
        self.local_conn = local_sock
        self.remote_conn = None
        self.config = config
        self.stage = self.STAGE_INIT
    
    def handle_init(self, data):
        if data != b'\x05\x01\x00':
            self.local_conn.send(b'\x05\xff')
            raise InitFailure
        self.local_conn.send(b'\x05\x00')
        self.remote_conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.remote_conn.connect((self.remote_addr, self.remote_port))
            
        except:
            raise RemoteClose
        self.stage = self.STAGE_STREAM

    def handle_stream(self, data):
        
        print("send server:", data)
        self.remote_conn.sendall(data)
        
        self.remote_conn.setblocking(0)
        server_data = b''
        while True:
            try:
                buf = self.remote_conn.recv(self.BUF_SIZE)
            except:
                break
            if not buf:
                break
            server_data += buf
     
        print("receive server:", (len(server_data)), server_data)
        self.local_conn.sendall(server_data)


    def handle_message(self, data):
        if self.stage == self.STAGE_INIT:
            self.handle_init(data)
        elif self.stage == self.STAGE_STREAM:
            self.handle_stream(data)

    def close(self):
        self.local_conn.close()
        if self.remote_conn:
            self.remote_conn.close()

    def run(self):
        while True:
            self.local_conn.settimeout(self.TIMEOUT)
            try:
                data = self.local_conn.recv(self.BUF_SIZE)
                if not data:
                    break
                else:
                    self.local_conn.settimeout(0)
                    self.handle_message(data)
            except TimeOut:
                print("timeout")
                break
            except InitFailure:
                print("Init failed")
                break
            except RemoteClose:
                print("RemoteClose")
                break
            except:
                break
        print("quit")
        self.close()
        
class Client:
    

    def __init__(self, config):
        self.local_addr = config["local_addr"]
        self.local_port = config["local_port"]

        self.local_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.local_socket.bind((self.local_addr,self.local_port))
        self.local_socket.listen(1024)
        print('Listening at {}:{}'.format(self.local_addr, self.local_port))


        self.remote_addr = config["server_addr"]
        self.remote_port = config["server_port"]
    
        self.cipher = Cipher()
        self.config = config

    def new_tcprelay(self, local_sock):
        local_sock.setblocking(0)
        tcp = ClientTCPRelay(self.config, local_sock)
        tcp.run()
        

    def loop(self):
        while True:
            local_sock, local_addr = self.local_socket.accept()
            t = threading.Thread(target = self.new_tcprelay, args=[local_sock])
            t.start()
            



def main():
    config = {"local_addr": "127.0.0.1",
              "local_port": 1080,
              "server_addr": "127.0.0.1",
              "server_port": 1234}
    client = Client(config)
    client.loop()


    
if __name__ == '__main__':
    main()