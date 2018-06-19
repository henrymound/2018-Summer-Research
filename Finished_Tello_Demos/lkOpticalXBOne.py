import sys
import traceback
import tellopy
import av
import cv2.cv2 as cv  # for avoidance of pylint error
import numpy as np
import pygame
import pygame.locals
import time
import video
from lib.common import anorm2, draw_str
from time import clock
import threading


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


    lk_params = dict( winSize  = (5, 5),
                      maxLevel = 2,
                      criteria = (cv.TERM_CRITERIA_EPS | cv.TERM_CRITERIA_COUNT, 10, 0.03))

    feature_params = dict( maxCorners = 200,
                           qualityLevel = 0.03,
                           minDistance = 7,
                           blockSize = 7 )

    try:
        drone.connect()
        drone.wait_for_connection(60.0)
        pygame.init()
        pygame.joystick.init()

        track_len = 10
        detect_interval = 5
        tracks = []
        frame_idx = 0
        VIDEO_SCALE = 0.5

        #drone.set_video_encoder_rate(2)
        container = av.open(drone.get_video_stream())

        js = pygame.joystick.Joystick(0)
        js.init()
        js_name = js.get_name()
        print('Joystick name: ' + js_name)


        while True:
            time.sleep(0.01)
            for frameRaw in container.decode(video=0):
                checkController()
                frame1 = cv.cvtColor(np.array(frameRaw.to_image()), cv.COLOR_RGB2BGR)
                frame = cv.resize(frame1, (0,0), fx=VIDEO_SCALE, fy=VIDEO_SCALE)
                frame_gray = cv.cvtColor(frame,cv.COLOR_BGR2GRAY)
                vis = frame.copy()

                if len(tracks) > 0:
                    img0, img1 = prev_gray, frame_gray
                    p0 = np.float32([tr[-1] for tr in tracks]).reshape(-1, 1, 2)
                    p1, _st, _err = cv.calcOpticalFlowPyrLK(img0, img1, p0, None, **lk_params)
                    p0r, _st, _err = cv.calcOpticalFlowPyrLK(img1, img0, p1, None, **lk_params)
                    d = abs(p0-p0r).reshape(-1, 2).max(-1)
                    good = d < 1
                    new_tracks = []

                    for tr, (x, y), good_flag in zip(tracks, p1.reshape(-1, 2), good):
                        if not good_flag:
                            continue
                        tr.append((x, y))
                        if len(tr) > track_len:
                            del tr[0]
                        new_tracks.append(tr)
                        cv.circle(vis, (x, y), 2, (0, 255, 0), -1)
                    tracks = new_tracks
                    cv.polylines(vis, [np.int32(tr) for tr in tracks], False, (0, 255, 0))
                    draw_str(vis, (20, 20), 'track count: %d' % len(tracks))

                if frame_idx % detect_interval == 0:
                    mask = np.zeros_like(frame_gray)
                    mask[:] = 255
                    for x, y in [np.int32(tr[-1]) for tr in tracks]:
                        cv.circle(mask, (x, y), 5, 0, -1)
                    p = cv.goodFeaturesToTrack(frame_gray, mask = mask, **feature_params)
                    if p is not None:
                        for x, y in np.float32(p).reshape(-1, 2):
                            tracks.append([(x, y)])

                frame_idx += 1
                prev_gray = frame_gray
                cv.imshow('Tello Dense Optical - Middlebury Research', vis)

                ch = cv.waitKey(1)
                if ch == 27:
                    break

    except Exception as ex:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        traceback.print_exception(exc_type, exc_value, exc_traceback)
        print(ex)

    finally:
        drone.quit()
        cv.destroyAllWindows()

if __name__ == '__main__':
    main()
