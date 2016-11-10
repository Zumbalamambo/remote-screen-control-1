import socket
import os
from screenfeed import ScreenFeed

host = '127.0.0.1'
port = 9090
buffer_length = 1000

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host, port))
sc = ScreenFeed('Teamviewer')

while True:
	frame = sc.get_frame()
	bytes_sent = 0
	len_sent = 0
	length = len(frame)
	length_str = str(length).zfill(10)

	while len_sent < 10:
		sent = s.send(length_str[len_sent:])
		if sent == 0:
			raise RuntimeError("Socket Connection Broken")
		len_sent += sent

	while bytes_sent < length:
		sent = s.send(frame[bytes_sent:])
		if sent == 0:
			raise RuntimeError("Socket Connection Broken")
		bytes_sent += sent







s.close()
