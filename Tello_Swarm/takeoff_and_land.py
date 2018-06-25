import socket
import time

sock1 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock1.setsockopt(socket.SOL_SOCKET, 25, 'lo0:'.encode())

sock2 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock2.setsockopt(socket.SOL_SOCKET, 25, 'en8'.encode())

sock1.sendto('command'.encode(), 0, ('192.168.10.1', 8889))
sock2.sendto('command'.encode(), 0, ('192.168.10.1', 8889))

sock1.sendto('takeoff'.encode(), 0, ('192.168.10.1', 8889))
sock2.sendto('takeoff'.encode(), 0, ('192.168.10.1', 8889))

sock1.sendto('command'.encode(), 0, ('192.168.10.1', 8889))
sock2.sendto('command'.encode(), 0, ('192.168.10.1', 8889))

sock1.sendto('land'.encode(), 0, ('192.168.10.1', 8889))
sock2.sendto('land'.encode(), 0, ('192.168.10.1', 8889))
