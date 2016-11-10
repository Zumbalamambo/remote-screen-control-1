import socket
from screenfeed import ScreenFeed

host = '127.0.0.1'
port = 9090

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((host,port))
s.listen(5)

conn, addr = s.accept()
print 'Connection address:', addr
sc = ScreenFeed('Teamviewer')

while 1:
	tot_recv = 0
	len_recv = 0
	msg = []
	len_msg = []
	while len_recv < 10:
		chunk = conn.recv(10 - tot_recv)
		if chunk == '':
			raise RuntimeError("Socket connection broken")
		len_msg.append(chunk)
		len_recv += len(chunk)
	len_str = ''.join(len_msg)
	length = int(len_str)

	while tot_recv < length:
		chunk = conn.recv(length - tot_recv)
		if chunk == '':
			raise RuntimeError("Socket connection broken")
		msg.append(chunk)
		tot_recv += len(chunk)
	msg = ''.join(msg)
	sc.set_frame(msg)

conn.close()



