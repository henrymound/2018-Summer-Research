import sys
import traceback
import tellopy
import av
import cv2.cv2 as cv2  # for avoidance of pylint error
import numpy as np

class JoystickPS3:
    # d-pad
    UP = 4  # UP
    DOWN = 6  # DOWN
    ROTATE_LEFT = 7  # LEFT
    ROTATE_RIGHT = 5  # RIGHT

    # bumper triggers
    TAKEOFF = 11  # R1
    LAND = 10  # L1
    # UNUSED = 9 #R2
    # UNUSED = 8 #L2

    # buttons
    FORWARD = 12  # TRIANGLE
    BACKWARD = 14  # CROSS
    LEFT = 15  # SQUARE
    RIGHT = 13  # CIRCLE

    # axis
    LEFT_X = 0
    LEFT_Y = 1
    RIGHT_X = 2
    RIGHT_Y = 3
    LEFT_X_REVERSE = 1.0
    LEFT_Y_REVERSE = -1.0
    RIGHT_X_REVERSE = 1.0
    RIGHT_Y_REVERSE = -1.0
    DEADZONE = 0.1


class JoystickPS4:
    # d-pad
    UP = -1  # UP
    DOWN = -1  # DOWN
    ROTATE_LEFT = -1  # LEFT
    ROTATE_RIGHT = -1  # RIGHT

    # bumper triggers
    TAKEOFF = 5  # R1
    LAND = 4  # L1
    # UNUSED = 7 #R2
    # UNUSED = 6 #L2

    # buttons
    FORWARD = 3  # TRIANGLE
    BACKWARD = 1  # CROSS
    LEFT = 0  # SQUARE
    RIGHT = 2  # CIRCLE

    # axis
    LEFT_X = 0
    LEFT_Y = 1
    RIGHT_X = 2
    RIGHT_Y = 3
    LEFT_X_REVERSE = 1.0
    LEFT_Y_REVERSE = -1.0
    RIGHT_X_REVERSE = 1.0
    RIGHT_Y_REVERSE = -1.0
    DEADZONE = 0.08


class JoystickXONE:
    # d-pad
    UP = 0  # UP
    DOWN = 1  # DOWN
    ROTATE_LEFT = 2  # LEFT
    ROTATE_RIGHT = 3  # RIGHT

    # bumper triggers
    TAKEOFF = 9  # RB
    LAND = 8  # LB
    # UNUSED = 7 #RT
    # UNUSED = 6 #LT

    # buttons
    FORWARD = 14  # Y
    BACKWARD = 11  # A
    LEFT = 13  # X
    RIGHT = 12  # B

    # axis
    LEFT_X = 0
    LEFT_Y = 1
    RIGHT_X = 2
    RIGHT_Y = 3
    LEFT_X_REVERSE = 1.0
    LEFT_Y_REVERSE = -1.0
    RIGHT_X_REVERSE = 1.0
    RIGHT_Y_REVERSE = -1.0
    DEADZONE = 0.09



# Global variables
buttons = JoystickXONE
speed = 100
throttle = 0.0
yaw = 0.0
pitch = 0.0
roll = 0.0
drone = tellopy.Tello()


def update(old, new, max_delta=0.3):
    if abs(old - new) <= max_delta:
        res = new
    else:
        res = 0.0
    return res

def checkController():
    global buttons
    global speed
    global throttle
    global yaw
    global pitch
    global roll
    global drone

    for e in pygame.event.get():
        if e.type == pygame.locals.JOYAXISMOTION:
            # ignore small input values (Deadzone)
            if -buttons.DEADZONE <= e.value and e.value <= buttons.DEADZONE:
                e.value = 0.0
            if e.axis == buttons.LEFT_Y:
                throttle = update(
                    throttle, e.value * buttons.LEFT_Y_REVERSE)
                drone.set_throttle(throttle)
            if e.axis == buttons.LEFT_X:
                yaw = update(yaw, e.value * buttons.LEFT_X_REVERSE)
                drone.set_yaw(yaw)
            if e.axis == buttons.RIGHT_Y:
                pitch = update(pitch, e.value *
                               buttons.RIGHT_Y_REVERSE)
                drone.set_pitch(pitch)
            if e.axis == buttons.RIGHT_X:
                roll = update(roll, e.value * buttons.RIGHT_X_REVERSE)
                drone.set_roll(roll)

        elif e.type == pygame.locals.JOYHATMOTION:
            if e.value[0] < 0:
                drone.counter_clockwise(speed)
                print("cc")
            if e.value[0] == 0:
                drone.clockwise(0)
            if e.value[0] > 0:
                drone.clockwise(speed)
                print("c")
            if e.value[1] < 0:
                drone.down(speed)
            if e.value[1] == 0:
                drone.up(0)
            if e.value[1] > 0:
                drone.up(speed)
                print("up")
        elif e.type == pygame.locals.JOYBUTTONDOWN:
            if e.button == buttons.LAND:
                drone.land()
                print("land")
            elif e.button == buttons.UP:
                drone.up(speed)
                print("up")
            elif e.button == buttons.DOWN:
                drone.down(speed)
                print("down")
            elif e.button == buttons.ROTATE_RIGHT:
                drone.clockwise(speed)
                print("c")
            elif e.button == buttons.ROTATE_LEFT:
                drone.counter_clockwise(speed)
                print("cc")
            elif e.button == buttons.FORWARD:
                drone.forward(speed)
                print("forward")
            elif e.button == buttons.BACKWARD:
                drone.backward(speed)
                print("backward")
            elif e.button == buttons.RIGHT:
                drone.right(speed)
                print("right")
            elif e.button == buttons.LEFT:
                drone.left(speed)
                print("left")
        elif e.type == pygame.locals.JOYBUTTONUP:
            if e.button == buttons.TAKEOFF:
                drone.takeoff()
                print("takeoff")
            elif e.button == buttons.UP:
                drone.up(0)
            elif e.button == buttons.DOWN:
                drone.down(0)
            elif e.button == buttons.ROTATE_RIGHT:
                drone.clockwise(0)
            elif e.button == buttons.ROTATE_LEFT:
                drone.counter_clockwise(0)
            elif e.button == buttons.FORWARD:
                drone.forward(0)
            elif e.button == buttons.BACKWARD:
                drone.backward(0)
            elif e.button == buttons.RIGHT:
                drone.right(0)
            elif e.button == buttons.LEFT:
                drone.left(0)


def main():
    drone = tellopy.Tello()

    try:
        drone.connect()
        drone.wait_for_connection(60.0)
        pygame.init()
        pygame.joystick.init()

        container = av.open(drone.get_video_stream())
        frameCount = 0 # Stores the current frame being processed
        frame1 = None # Store variables for first frame
        frame2 = None # Store variables for second frame
        prvs = None
        hsv = None

        while True:
            for frame in container.decode(video=0):
                checkController()
                frameCount += 1
                if frameCount == 1: # If first frame
                    frame1 = cv2.cvtColor(np.array(frame.to_image()), cv2.COLOR_RGB2BGR)
                    prvs = cv2.cvtColor(frame1,cv2.COLOR_BGR2GRAY)
                    hsv = np.zeros_like(frame1)
                    hsv[...,1] = 255
                else: # If not first frame
                    frame2 = cv2.cvtColor(np.array(frame.to_image()), cv2.COLOR_RGB2BGR)
                    next = cv2.cvtColor(frame2,cv2.COLOR_BGR2GRAY)
                    flow = cv2.calcOpticalFlowFarneback(prvs,next, None, 0.5, 3, 15, 3, 5, 1.2, 0)
                    mag, ang = cv2.cartToPolar(flow[...,0], flow[...,1])
                    hsv[...,0] = ang*180/np.pi/2
                    hsv[...,2] = cv2.normalize(mag,None,0,255,cv2.NORM_MINMAX)
                    bgr = cv2.cvtColor(hsv,cv2.COLOR_HSV2BGR)
                    cv2.imshow('frame2',bgr)
                    k = cv2.waitKey(30) & 0xff
                    if k == 27:
                        break
                    elif k == ord('s'):
                        cv2.imwrite('opticalfb.png',frame2)
                        cv2.imwrite('opticalhsv.png',bgr)
                    prvs = next
                print(frameCount)

    except Exception as ex:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        traceback.print_exception(exc_type, exc_value, exc_traceback)
        print(ex)
    finally:
        drone.quit()
        cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
