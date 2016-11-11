import socket
import os
from screenfeed import ScreenFeed
import time
import pyautogui


host = ''
port_1 = 9090
port_2 = 9091
port_3 = 9092
broadcast_port = 10100
host_default = ''
buffer_length = 1000000000

#Broadcasting to server
port = 10100
msg = socket.gethostbyname(socket.gethostname())
dest = ('<broadcast>',port)
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
s.sendto(msg, dest)
s.close()

#Receving Broadcast from client
TCP_IP = ''
TCP_IP_2 = ''
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
s.bind((TCP_IP_2,port))
message, address = s.recvfrom(10104)            
ad = ''.join(str(address));
ad1 = ad.split()
ad2= ad1[0]
ad3=ad2[2:15]
ad3 = ad3.replace("'", "")
ad3 = ad3.replace(",", "")
TCP_IP_2 = str(ad3)
TCP_IP = message
print TCP_IP_2
print TCP_IP
host = TCP_IP
s.close()
time.sleep(1)





# Socket for receiving mouse events
soc_event = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
soc_event.connect((host, port_1))

#Socket for sending frames
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host, port_2))

#Socket for sending frame sizes
soc_frame_size = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
soc_frame_size.connect((host, port_3))


#Sending screen size so that the user can resize the screen
screen_width, screen_height = pyautogui.size()
wsent = 0
hsent = 0
heightstr = str(screen_height).zfill(8)
widthstr = str(screen_width).zfill(8)

while hsent < 8:
	sent = soc_frame_size.send(heightstr[hsent:])
	if sent == 0:
		raise RuntimeError("Socket connection broken")
	hsent += sent
while wsent < 8:
	sent = soc_frame_size.send(widthstr[wsent:])
	if sent == 0:
		raise RuntimeError("Socket connection broken")
	wsent += sent

soc_frame_size.close()


#Sending frames in parent and receiving mouse clicks in child
sc = ScreenFeed('Teamviewer')
pid = os.fork()
if(pid!=0):
	
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

else:

	
	while True:
		try:
			type = soc_event.recv(2)
			type = int(type)
			if type == 1:
				x = soc_event.recv(4)
				x = int(x)
				y = soc_event.recv(4)
				y = int(y)
				pyautogui.moveTo(x,y)
				pyautogui.click()
			if type == 2:
				x = soc_event.recv(4)
				x = int(x)
				y = soc_event.recv(4)
				y = int(y)
				pyautogui.moveTo(x,y)
				pyautogui.click(button='right')
		except Exception as error:
			print ("Error is:", a)  
		
s.close()
soc_frame_size.close()
soc_event.close()
