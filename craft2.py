import socket

UDP_IP_ADDRESS = "88.205.225.205"
UDP_PORT_NO = 6789
Message = b"Hello, Server"

clientSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
clientSock.sendto(Message, (UDP_IP_ADDRESS, UDP_PORT_NO))