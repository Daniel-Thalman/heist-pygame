import socket


# TCP_IP = 'jamulan.com'
# TCP_PORT = 5005
# BUFFER_SIZE = 1024
# MESSAGE = str.encode("Hello, World!")
#
# s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# s.connect((TCP_IP, TCP_PORT))
# s.send(MESSAGE)
# data = s.recv(BUFFER_SIZE)
# s.close()
#
# print("received data:", data)

UDP_IP = "jamulan.com"
UDP_PORT = 5005
MESSAGE = str.encode("Hello, World!")

print("UDP target IP:", UDP_IP)
print("UDP target port:", UDP_PORT)
print("message:", MESSAGE)

sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP
# sock.sendto(MESSAGE, (UDP_IP, UDP_PORT))

while 1:
	sock.sendto(str.encode('200'), (UDP_IP, UDP_PORT))