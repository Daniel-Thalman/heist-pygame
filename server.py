import socket
# This file is unneccessary but was where testing happened

# TCP_IP = 'jamulan.com'
# TCP_PORT = 5005
# BUFFER_SIZE = 20  # Normally 1024, but we want fast response
#
# s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# s.bind((TCP_IP, TCP_PORT))
# s.listen(1)
#
# conn, addr = s.accept()
# print('Connection address:', addr)
# while 1:
#     data = conn.recv(BUFFER_SIZE)
#     if not data: break
#     print("received data:", data)
#     conn.send(data)  # echo
# conn.close()

UDP_IP = "jamulan.com"
UDP_PORT = 5005

sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP
sock.bind((UDP_IP, UDP_PORT))

while True:
    data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
    print("received message:", data)
