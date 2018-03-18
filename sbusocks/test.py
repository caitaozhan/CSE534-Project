import socket
import time

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
while True:
    s.connect(('127.0.0.1', 1080))
    while True:
        s.send(b'Hello!')
        time.sleep(2)


