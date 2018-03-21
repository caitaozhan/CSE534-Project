import argparse
import threading
import socket
from cipher import Cipher
import select
import sys
import pdb


def int_from_bytes(bytes_object):
    return int.from_bytes(bytes_object, byteorder='big')

class ConnectionFailure(Exception):
    pass

class RemoteClose(Exception):
    pass

class TimeOut(Exception):
    pass



class SocksPacket:
    def __init__(self, data):
        self.data = data
    def unpack(self):
        self.version = self.data[0]
        self.cmd = self.data[1]
        self.des
    def pack(self):
        pass

class ServerTCPRelay:
    TIMEOUT = 5
    BUF_SIZE = 32 * 1024
    STAGE_CONNECTION = 0
    STAGE_STREAM = 1

    def __init__(self, config, local_sock):
        self.local_addr = config["local_addr"]
        self.local_port = config["local_port"]
        self.local_conn = local_sock
        self.remote_conn = None
        self.config = config
        self.stage = self.STAGE_CONNECTION
        self.version = None
        self.server_addr = None
        self.server_port = None

    def handle_connection(self, data):
        if data[:3] == b'\x05\x01\x00':
            if data[3] == 0x03:
                domain_len = int(data[4])
                self.server_addr = socket.gethostbyname(data[5:5 + domain_len])
                self.server_port = int_from_bytes(data[-2:])
                print("Connecting {}:{}".format(self.server_addr, self.server_port))
                self.remote_conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

            elif data[3] == 0x01:
                seg = []
                for i in range(4):
                    seg.append(str(int(data[4+i])))
                self.server_addr = '.'.append(seg)
                self.server_port = int_from_bytes(data[-2:])
                self.remote_conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            else:
                raise ConnectionFailure
            
            try:
                self.remote_conn.connect((self.server_addr, self.server_port))
                self.remote_conn.setblocking(0)
                print("Connecting {}:{}".format(self.server_addr, self.server_port))
                self.local_conn.send(b'\x05\x00\x00\x01\x00\x00\x00\x00\x00\x00')
                self.stage = self.STAGE_STREAM
            except:
                raise ConnectionFailure

        else:
            self.local_conn.send(b'\x05\x05\x00\x01\x00\x00\x00\x00\x00\x00')
                


    def handle_stream(self, data):
        print("send server:", data)
        self.remote_conn.sendall(data)
        
        server_data = b''
        self.remote_conn.setblocking(0)
        while True:
            try:
                buf = self.remote_conn.recv(self.BUF_SIZE)
            except:
                break
            if not buf:
                break
            server_data += buf
        else:
            self.remote_conn.settimeout(0)      
            print("receive server:", server_data)
            self.local_conn.sendall(server_data)


    def handle_message(self, data):
        if self.stage == self.STAGE_CONNECTION:
            self.handle_connection(data)
        else:
            self.handle_stream(data)

    def close(self):
        self.local_conn.close()
        if self.remote_conn is not None:
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
            except ConnectionFailure:
                print("connect failed")
                break
            except RemoteClose:
                print("RemoteClose")
                break
            except:
                break
        self.close()
        print("quit")

        
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

    def new_tcprelay(self, local_sock):
        local_sock.setblocking(0)
        tcp = ServerTCPRelay(self.config, local_sock)
        tcp.run()
        

    def loop(self):
        while True:
            local_sock, local_addr = self.local_socket.accept()
            t = threading.Thread(target = self.new_tcprelay, args=[local_sock])
            t.start()
            



def main():
    config = {"local_addr": "0.0.0.0",
              "local_port": 1234}
    server = Server(config)
    server.loop()


    
if __name__ == '__main__':
    main()