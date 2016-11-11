import socket
import time
import os,sys
import PIL
import Tkinter as tk
import io
import pyxhook
import cv2
import numpy as np
from PIL import Image, ImageTk
from screenfeed import ScreenFeed
import traceback



host = ''
port_1 = 9090
port_2 = 9091
port_3 = 9092
broadcast_port = 10100
host_default = ''
buffer_length = 1000000000

#Receving broadcast from client
TCP_IP = ''
port = 10100
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
s.bind((TCP_IP,port))
message, address = s.recvfrom(10104)            
ad = ''.join(str(address));
ad1 = ad.split()
ad2= ad1[0]
ad3=ad2[2:15]
s.close()
ad3 = ad3.replace("'", "")
ad3 = ad3.replace(",", "")
TCP_IP = str(ad3)

#Sending broadcast to server
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(('8.8.8.8', 0))
msg = s.getsockname()[0]
TCP_IP = msg
print TCP_IP
dest = ('<broadcast>',10100)
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
s.sendto(TCP_IP, dest)
host = TCP_IP
s.close()


#Socket for sending mouse events
soc_event = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
soc_event.bind((host,port_1))
soc_event.listen(5)


#Socket for receiving frames
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((host,port_2))
s.listen(5)


#Socket for receiving frame size
soc_recv_size = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
soc_recv_size.bind((host,port_3))
soc_recv_size.listen(5)


conn1, addr1 = soc_recv_size.accept()
print 'Connection address for receiving frame sizes:', addr1

#Receiving Frame Sizes
hrec = 0
wrec = 0
harray = []
warray = []
while hrec < 8:
	chunk = conn1.recv(8 - hrec)
	if chunk == '':
		raise RuntimeError("Socket connection broken")
	harray.append(chunk)
	hrec +=  len(chunk)
heightstr = ''.join(harray)
screen_height = int(heightstr)
while wrec < 8:
	chunk = conn1.recv(8 - wrec)
	if chunk == '':
		raise RuntimeError("Socket connection broken")
	warray.append(chunk)
	wrec +=  len(chunk)
widthstr = ''.join(warray)
screen_width = int(widthstr)
conn1.close()
soc_recv_size.close()

root = tk.Tk()
root.geometry(str(screen_width) + "x" + str(screen_height))



conn2, addr2 = soc_event.accept()
print 'Connection address for sending frame sizes:', addr2
conn, addr = s.accept()
print 'Connection address for receiving frames:', addr
sc = ScreenFeed('Teamviewer')

#Sending Events for left, right mouse clicks and keyboards
def left(event):
	type = 1
	conn2.send(str(type).zfill(2))
	conn2.send(str(event.x).zfill(4))
	conn2.send(str(event.y).zfill(4))

def right(event):
	type = 2
	conn2.send(str(type).zfill(2))
	conn2.send(str(event.x).zfill(4))
	conn2.send(str(event.y).zfill(4))

def kbevent( event ):
    	type = 0
	conn1.send(str(type).zfill(2))  	
	conn1.send(event.Key)

def quit(event):
	print ("Double Click, so let's stop", repr(event))

#Receving frames and displaying it
counter = 0
pid = os.fork()
if(pid != 0):
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
		pil_bytes = io.BytesIO(msg)
		pil_image = Image.open(pil_bytes)
		img_np = np.array(pil_image)
		frame = cv2.cvtColor(np.array(img_np), cv2.COLOR_GRAY2RGB)
		pil_image = Image.fromarray(frame)
		pil_image = pil_image.resize((screen_width,screen_height), PIL.Image.ANTIALIAS)
		photo = ImageTk.PhotoImage(image = pil_image)	
		if (counter == 0) :	
				label = tk.Label(root, image= photo)
				label.bind('<Button-1>', left)
	 			label.bind('<Button-3>', right)
				label.grid()
				label.update()
		else:
				label.configure(image = photo)
				label.image = photo
				label.update()
		counter = counter + 1
		conn.close
else:

	hookman = pyxhook.HookManager()
	hookman.KeyDown = kbevent
	hookman.HookKeyboard()
	hookman.start()
	running = True
	while running:
		time.sleep(0.1)
	hookman.cancel()

    
root.mainloop()

s.close()
soc_event.close()




