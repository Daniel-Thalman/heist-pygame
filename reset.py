import socket

TCP_IP = "jamulan.com"
TCP_PORT = 5005

sock = socket.socket(socket.AF_INET, # Internet
				 socket.SOCK_STREAM) # TCP

sock.close()
