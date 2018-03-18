import socket
import sbu
import time

class TCPRelay:
	TIME_OUT = 5
	BUF_SIZE = 32 * 1024

    def __init__(self, config):
        self.local_sock = config["local_sock"]
        self.remote_sock = config["remote_sock"]
        self.is_client = config["is_client"]
        self.cipher = config["cipher"]
        self.active = True

    def run(self):
    	while True:
    		if is_client:
    			local_data = self.local_sock.recv(self.BUF_SIZE)
    			local_data = self.cipher.encrypt(local_data)
    			self.remote_sock.send(local_data)

    			remote_data = self.remote_sock.recv(self.BUF_SIZE)
    			remote_data = self.cipher.decrypt(remote_data)
    			self.local_sock.send(remote_data)

    		else:
    			local_data = self.local_sock.recv(self.BUF_SIZE)
    			local_data = self.cipher.decrypt(local_data)
    			self.remote_sock.send(local_data)

    			remote_data = self.remote_sock.recv(self.BUF_SIZE)
    			remote_data = self.cipher.encrypt(remote_data)
    			self.local_sock.send(remote_data)

    	self.active = False
    	


    
