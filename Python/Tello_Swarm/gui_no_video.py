from tkinter import *
import tellopy
import _thread
import time
import socket
import threading
import traceback

class Tello:
    """Wrapper to simply interactions with the Ryze Tello drone."""

    def __init__(self, wifiInterface, imperial=True, command_timeout=.3, tello_ip='192.168.10.1', tello_port=8889):
        """Binds to the local IP/port and puts the Tello into command mode.

        Args:
            local_ip (str): Local IP address to bind.
            local_port (int): Local port to bind.
            imperial (bool): If True, speed is MPH and distance is feet.
                             If False, speed is KPH and distance is meters.
            command_timeout (int|float): Number of seconds to wait for a response to a command.
            tello_ip (str): Tello IP.
            tello_port (int): Tello port.

        Raises:
            RuntimeError: If the Tello rejects the attempt to enter command mode.

        """

        self.abort_flag = False
        self.command_timeout = command_timeout
        self.imperial = imperial
        self.response = None
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.setsockopt(socket.SOL_SOCKET, 25, wifiInterface.encode())
        #self.tello_address = (tello_ip, tello_port)

        #self.socket.bind((local_ip, local_port))

        self.receive_thread = threading.Thread(target=self._receive_thread)
        self.receive_thread.daemon=True

        self.receive_thread.start()

        if self.send_command('command') != 'OK':
            raise RuntimeError('Tello rejected attempt to enter command mode')

    def __del__(self):
        """Closes the local socket."""

        self.socket.close()

    def _receive_thread(self):
        """Listens for responses from the Tello.

        Runs as a thread, sets self.response to whatever the Tello last returned.

        """
        while True:
            try:
                self.response, ip = self.socket.recvfrom(256)
            except Exception:
                break

    def flip(self, direction):
        """Flips.

        Args:
            direction (str): Direction to flip, 'l', 'r', 'f', 'b', 'lb', 'lf', 'rb' or 'rf'.

        Returns:
            str: Response from Tello, 'OK' or 'FALSE'.

        """

        return self.send_command('flip %s' % direction)

    def get_battery(self):
        """Returns percent battery life remaining.

        Returns:
            int: Percent battery life remaining.

        """

        battery = self.send_command('battery?')

        try:
            battery = int(battery)
        except:
            pass

        return battery


    def get_flight_time(self):
        """Returns the number of seconds elapsed during flight.

        Returns:
            int: Seconds elapsed during flight.

        """

        flight_time = self.send_command('time?')

        try:
            flight_time = int(flight_time)
        except:
            pass

        return flight_time

    def get_speed(self):
        """Returns the current speed.

        Returns:
            int: Current speed in KPH or MPH.

        """

        speed = self.send_command('speed?')

        try:
            speed = float(speed)

            if self.imperial is True:
                speed = round((speed / 44.704), 1)
            else:
                speed = round((speed / 27.7778), 1)
        except:
            pass

        return speed

    def land(self):
        """Initiates landing.

        Returns:
            str: Response from Tello, 'OK' or 'FALSE'.

        """

        return self.send_command('land')

    def move(self, direction, distance):
        """Moves in a direction for a distance.

        This method expects meters or feet. The Tello API expects distances
        from 20 to 500 centimeters.

        Metric: .1 to 5 meters
        Imperial: .7 to 16.4 feet

        Args:
            direction (str): Direction to move, 'forward', 'back', 'right' or 'left'.
            distance (int|float): Distance to move.

        Returns:
            str: Response from Tello, 'OK' or 'FALSE'.

        """

        distance = float(distance)

        if self.imperial is True:
            distance = int(round(distance * 30.48))
        else:
            distance = int(round(distance * 100))

        return self.send_command('%s %s' % (direction, distance))

    def move_backward(self, distance):
        """Moves backward for a distance.

        See comments for Tello.move().

        Args:
            distance (int): Distance to move.

        Returns:
            str: Response from Tello, 'OK' or 'FALSE'.

        """

        return self.move('back', distance)

    def move_down(self, distance):
        """Moves down for a distance.
, self.tello_address
        See comments for Tello.move().

        Args:
            distance (int): Distance to move.

        Returns:
            str: Response from Tello, 'OK' or 'FALSE'.

        """

        return self.move('down', distance)

    def move_forward(self, distance):
        """Moves forward for a distance.

        See comments for Tello.move().

        Args:
            distance (int): Distance to move.

        Returns:
            str: Response from Tello, 'OK' or 'FALSE'.

        """
        return self.move('forward', distance)

    def move_left(self, distance):
        """Moves left for a distance.

        See comments for Tello.move().

        Args:
            distance (int): Distance to move.

        Returns:
            str: Response from Tello, 'OK' or 'FALSE'.

        """
        return self.move('left', distance)

    def move_right(self, distance):
        """Moves right for a distance.

        See comments for Tello.move().

        Args:
            distance (int): Distance to move.

        """
        return self.move('right', distance)

    def move_up(self, distance):
        """Moves up for a distance.

        See comments for Tello.move().

        Args:
            distance (int): Distance to move.

        Returns:
            str: Response from Tello, 'OK' or 'FALSE'.

        """

        return self.move('up', distance)

    def send_command(self, command):
        """Sends a command to the Tello and waits for a response.

        If self.command_timeout is exceeded before a response is received,
        a RuntimeError exception is raised.

        Args:
            command (str): Command to send.

        Returns:
            str: Response from Tello.

        Raises:
            RuntimeError: If no response is received within self.timeout seconds.

        """

        self.abort_flag = False
        timer = threading.Timer(self.command_timeout, self.set_abort_flag)

        self.socket.sendto(command.encode(), 0, ('192.168.10.1', 8889))

        timer.start()

        while self.response is None:
            if self.abort_flag is True:
                raise RuntimeError('No response to command')

        timer.cancel()

        response = self.response.decode('utf-8')
        self.response = None

        return response

    def set_abort_flag(self):
        """Sets self.abort_flag to True.

        Used by the timer in Tello.send_command() to indicate to that a response
        timeout has occurred.

        """

        self.abort_flag = True

    def set_speed(self, speed):
        """Sets speed.

        This method expects KPH or MPH. The Tello API expects speeds from
        1 to 100 centimeters/second.

        Metric: .1 to 3.6 KPH
        Imperial: .1 to 2.2 MPH

        Args:
            speed (int|float): Speed.

        Returns:
            str: Response from Tello, 'OK' or 'FALSE'.

        """

        speed = float(speed)

        if self.imperial is True:
            speed = int(round(speed * 44.704))
        else:
            speed = int(round(speed * 27.7778))

        return self.send_command('speed %s' % speed)

    def takeoff(self):
        """Initiates take-off.

        Returns:
            str: Response from Tello, 'OK' or 'FALSE'.

        """, self.tello_address

        return self.send_command('takeoff')

    def rotate_cw(self, degrees):
        """Rotates clockwise.

        Args:
            degrees (int): Degrees to rotate, 1 to 360.

        Returns:
            str: Response from Tello, 'OK' or 'FALSE'.

        """

        return self.send_command('cw %s' % degrees)

    def rotate_ccw(self, degrees):
        """Rotates counter-clockwise.

        Args:
            degrees (int): Degrees to rotate, 1 to 360.

        Returns:
            str: Response from Tello, 'OK' or 'FALSE'.

        """
        return self.send_command('ccw %s' % degrees)

drone1 = None
drone2 = None


def takeoffDrone1():
    global drone1
    drone1.takeoff()

def takeoffDrone2():
    global drone2
    drone2.takeoff()

def landDrone1():
    global drone1
    drone1.land()

def landDrone2():
    global drone2
    drone2.land()

def flipDrone1():
    global drone1
    drone1.flip("f")

def flipDrone2():
    global drone2
    drone2.flip("f")

root = Tk()
root.title("Tello 2 Drone Control")

drone1BatteryLabel = Label(root, text="NOT CONNECTED")
drone1BatteryLabel.grid(row=0, column=0, columnspan=1, sticky=N)
drone2BatteryLabel = Label(root, text="NOT CONNECTED")
drone2BatteryLabel.grid(row=0, column=1, columnspan=1, sticky=N)

def refreshBatteryDrone1():
    global drone1BatteryLabel
    global drone1
    while True:
        time.sleep(5)
        drone1BatteryLabel.config(text=("Battery of Drone 1: %s" % drone1.get_battery()))

def refreshBatteryDrone2():
    global drone2BatteryLabel
    global drone2
    while True:
        time.sleep(5)
        drone2BatteryLabel.config(text=("Battery of Drone 2: %s" % drone2.get_battery()))

def connectDrone1():
    global drone1
    drone1 = Tello("wlp1s0")
    print("Battery of Drone 1: %s" % drone1.get_battery())
    _thread.start_new_thread(refreshBatteryDrone1, ())

def connectDrone2():
    global drone2
    drone2 = Tello("wlxf8788c004f09")
    print("Battery of Drone 2: %s" % drone2.get_battery())
    _thread.start_new_thread(refreshBatteryDrone2, ())

# Drone 1 Buttons
connectDrone1Button = Button(root, text="Connect Drone 1", command=connectDrone1)
connectDrone1Button.grid(row=1, column=0, columnspan=1, sticky=N)
takeoffDrone1Button = Button(root, text="Takeoff Drone 1", command=takeoffDrone1)
takeoffDrone1Button.grid(row=2, column=0, columnspan=1, sticky=N)
landDrone1Button = Button(root, text="Land Drone 1", command=landDrone1)
landDrone1Button.grid(row=3, column=0, columnspan=1, sticky=N)
flipDrone1Button = Button(root, text="Flip Drone 1", command=flipDrone1)
flipDrone1Button.grid(row=4, column=0, columnspan=1, sticky=N)

# Drone 2 Buttons
connectDrone2Button = Button(root, text="Connect Drone 2", command=connectDrone2)
connectDrone2Button.grid(row=1, column=1, columnspan=1, sticky=N)
takeoffDrone2Button = Button(root, text="Takeoff Drone 2", command=takeoffDrone2)
takeoffDrone2Button.grid(row=2, column=1, columnspan=1, sticky=N)
landDrone2Button = Button(root, text="Land Drone 2", command=landDrone2)
landDrone2Button.grid(row=3, column=1, columnspan=1, sticky=N)
flipDrone2Button = Button(root, text="Flip Drone 2", command=flipDrone2)
flipDrone2Button.grid(row=4, column=1, columnspan=1, sticky=N)

# Main loop
mainloop()
