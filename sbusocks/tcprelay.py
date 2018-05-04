import socket
from cipher import Cipher
import select
from utility import int_from_bytes


class InitFailure(Exception):
    pass

class RemoteClose(Exception):
    pass

class TimeOut(Exception):
    pass

class NoData(Exception):
    pass


class TCPRelay:
    TIMEOUT = 60
    BUF_SIZE = 32 * 1024
    STAGE_STREAM = 2
    STAGE_CONNECTION = 1
    STAGE_INIT = 0

    def __init__(self, config, local_sock):
        self.is_client = config["is_client"]
        self.local_addr = config["local_addr"]
        self.local_port = config["local_port"]

        if self.is_client:
            self.remote_addr = config["server_addr"]
            self.remote_port = config["server_port"]
        
        self.local_conn = local_sock
        self.remote_conn = None
        self.config = config
        if self.is_client:
            self.stage = self.STAGE_INIT
        else:
            self.stage = self.STAGE_CONNECTION

        self.domain = None
    

    def handle_init(self, data):
        if data != b'\x05\x01\x00':
            self.local_conn.send(b'\x05\xff')
            raise InitFailure
        self.local_conn.send(b'\x05\x00')
        self.remote_conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.remote_conn.connect((self.remote_addr, self.remote_port))
        self.stage = self.STAGE_STREAM


    def handle_connection(self, data):
        if data[:3] == b'\x05\x01\x00':
            if data[3] == 0x03:
                domain_len = int(data[4])
                self.domain = data[5:5 + domain_len]
                self.remote_addr = socket.gethostbyname(self.domain)
                self.server_port = int_from_bytes(data[-2:])
                print("Connecting {}:{} from {}:{}".format(self.domain, self.server_port, self.local_addr, self.local_port))
                self.remote_conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

            elif data[3] == 0x01:
                seg = []
                for i in range(4):
                    seg.append(str(int(data[4+i])))
                self.remote_addr = '.'.append(seg)
                self.server_port = int_from_bytes(data[-2:])
                print("Connecting {}:{} from {}:{}".format(self.remote_addr, self.server_port, self.local_addr, self.local_port))
                self.remote_conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            else:
                raise ConnectionFailure
            
            try:
                self.remote_conn.connect((self.remote_addr, self.server_port))
                self.local_conn.send(b'\x05\x00\x00\x01\x00\x00\x00\x00\x00\x00')
                self.stage = self.STAGE_STREAM
            except:
                raise ConnectionFailure

        else:
            self.local_conn.send(b'\x05\x05\x00\x01\x00\x00\x00\x00\x00\x00')


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
        elif self.stage == self.STAGE_CONNECTION:
            self.handle_connection(data)
        else:
            self.remote_conn.sendall(data)

    def close(self):
        self.local_conn.close()
        if self.remote_conn:
            self.remote_conn.close()

    def run(self):
        while True:
            # waiting list
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
        self.close()

