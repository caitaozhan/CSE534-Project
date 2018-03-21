import argparse
import threading
import socket
from cipher import Cipher
import select
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
    TIMEOUT = 10
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
                
                self.target_addr = None
                self.target_port = int_from_bytes(data[-2:])
                print(data[3:-2], self.target_port)

                #socket.gethostbyname(host)
        else:
            raise ConnectionFailure


    def handle_stream(self, data):
        socks_packet = SocksPacket(data)

        self.remote_conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.remote_conn.connect((self.remote_addr, self.remote_port))
        except:
            raise RemoteClose
        self.remote_conn.send(data)
        remote_ready = select.select([self.remote_conn], [], [], self.TIMEOUT)
        if remote_ready[0]:
            data = self.remote_conn.recv(self.BUF_SIZE)
        else:
            raise TimeOut


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
            local_ready = select.select([self.local_conn], [], [], self.TIMEOUT)
            if local_ready[0]:
                data = self.local_conn.recv(self.BUF_SIZE)
            else:
                break
            try:
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