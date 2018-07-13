import socket
import time

leftDrone = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
leftDrone.setsockopt(socket.SOL_SOCKET, 25, 'wlp1s0'.encode())

rightDrone = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
rightDrone.setsockopt(socket.SOL_SOCKET, 25, 'wlxf8788c004f09'.encode())

leftDrone.sendto('command'.encode(), 0, ('192.168.10.1', 8889))
rightDrone.sendto('command'.encode(), 0, ('192.168.10.1', 8889))

leftDrone.sendto('takeoff'.encode(), 0, ('192.168.10.1', 8889))
rightDrone.sendto('takeoff'.encode(), 0, ('192.168.10.1', 8889))

time.sleep(5)

leftDrone.sendto('command'.encode(), 0, ('192.168.10.1', 8889))
rightDrone.sendto('command'.encode(), 0, ('192.168.10.1', 8889))

leftDrone.sendto('down 50'.encode(), 0, ('192.168.10.1', 8889))
rightDrone.sendto('up 50'.encode(), 0, ('192.168.10.1', 8889))

time.sleep(5)

leftDrone.sendto('command'.encode(), 0, ('192.168.10.1', 8889))
rightDrone.sendto('command'.encode(), 0, ('192.168.10.1', 8889))

leftDrone.sendto('right 50'.encode(), 0, ('192.168.10.1', 8889))
rightDrone.sendto('left 50'.encode(), 0, ('192.168.10.1', 8889))

time.sleep(5)

leftDrone.sendto('command'.encode(), 0, ('192.168.10.1', 8889))
rightDrone.sendto('command'.encode(), 0, ('192.168.10.1', 8889))

leftDrone.sendto('up 50'.encode(), 0, ('192.168.10.1', 8889))
rightDrone.sendto('down 50'.encode(), 0, ('192.168.10.1', 8889))

time.sleep(5)

leftDrone.sendto('command'.encode(), 0, ('192.168.10.1', 8889))
rightDrone.sendto('command'.encode(), 0, ('192.168.10.1', 8889))

leftDrone.sendto('land'.encode(), 0, ('192.168.10.1', 8889))
rightDrone.sendto('land'.encode(), 0, ('192.168.10.1', 8889))
