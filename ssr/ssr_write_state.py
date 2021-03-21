#!/home/pi/venvs/rpi/bin/python
from ssr import SSR
import socket
import datetime

ssr1 = SSR(17)
ssr2 = SSR(27)

HOST = '127.0.0.1'
PORT = 2003

now = datetime.datetime.now()
msg1 = 'solar.ssr1.state {} {}\n'.format(
    ssr1.state, now.strftime('%s'))
msg2 = 'solar.ssr2.state {} {}\n'.format(
    ssr2.state, now.strftime('%s'))

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    s.sendall(msg1.encode('ascii'))
print(msg1)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    s.sendall(msg2.encode('ascii'))
print(msg2)

