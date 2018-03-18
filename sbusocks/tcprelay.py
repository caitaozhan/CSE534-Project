import socket
import sbu

class TCPRelay:
    def __init__(self, config):
        self.is_client = config["is_client"]
        self.listen_addr = config["listen_addr"]
        self.listen_port = config["listen_port"]
    
