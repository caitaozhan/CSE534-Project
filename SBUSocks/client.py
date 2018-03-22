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

class NoData(Exception):
    pass

class ClientTCPRelay:
    TIMEOUT = 60
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

        self.remote_conn.connect((self.remote_addr, self.remote_port))
        self.stage = self.STAGE_STREAM

    def handle_remote_stream(self, sock):
        data = sock.recv(self.BUF_SIZE)
        if not data:
            raise NoData
        self.local_conn.sendall(data)

    def handle_local_stream(self, sock):
        data = sock.recv(self.BUF_SIZE)
        if not data:
            raise NoData
        if self.stage == self.STAGE_INIT:
            self.handle_init(data)
        else:
            self.remote_conn.sendall(data)

    def close(self):
        self.local_conn.close()
        if self.remote_conn:
            self.remote_conn.close()

    def run(self):
        while True:
            rlist = [self.local_conn]
            if self.remote_conn:
                rlist.append(self.remote_conn)
            read_ready = select.select(rlist,[],[],self.TIMEOUT)
            if read_ready[0]:
                conn = read_ready[0][0]
                try:
                    if conn == self.local_conn:
                        self.handle_local_stream(conn)
                    else:
                        self.handle_remote_stream(conn)
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
            else:
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
        tcp = ClientTCPRelay(self.config, local_sock)
        tcp.run()
        

    def loop(self):
        while True:
            local_sock, local_addr = self.local_socket.accept()
            t = threading.Thread(target = self.new_tcprelay, args=[local_sock])
            t.start()
            

def main():
    config = {"local_addr": "127.0.0.1",
              "local_port": 1081,
              "server_addr": "45.32.154.172",
              "server_port": 9000}
    client = Client(config)
    client.loop()


    
if __name__ == '__main__':
    main()