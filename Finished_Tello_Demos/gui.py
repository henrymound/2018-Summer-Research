from tkinter import *
import pygame
import pygame.locals
import cv2.cv2 as cv
import av
import tellopy
from lib.common import anorm2, draw_str
from time import clock
import time
import traceback
import numpy as np
import lib.video
from PIL import Image, ImageTk

videoLabel = None
mainFrame = None
typeOfVideo = None

forwardLabel = None
backwardLabel = None
upLabel = None
downLabel = None
leftLabel = None
rightLabel = None

###################################################


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


###################################################


js = None
buttons = None


def connectController():  # A function that connects a game controller to the app
    global js
    global buttons
    pygame.init()
    pygame.joystick.init()
    try:
        js = pygame.joystick.Joystick(0)
        js.init()
        js_name = js.get_name()
        print('Joystick name: ' + js_name)
        if js_name in ('Wireless Controller', 'Sony Computer Entertainment Wireless Controller'):
            buttons = JoystickPS4
        elif js_name in ('PLAYSTATION(R)3 Controller', 'Sony PLAYSTATION(R)3 Controller'):
            buttons = JoystickPS3
        elif js_name == 'Xbox One Wired Controller':
            buttons = JoystickXONE
    except pygame.error:
        pass
    if buttons is None:
        print('no supported joystick found')
        return

###################################################


lk_params = dict(winSize=(5, 5),
                 maxLevel=2,
                 criteria=(cv.TERM_CRITERIA_EPS | cv.TERM_CRITERIA_COUNT, 10, 0.03))

feature_params = dict(maxCorners=200,
                      qualityLevel=0.03,
                      minDistance=30,
                      blockSize=7)


def update(old, new, max_delta=0.3):
    if abs(old - new) <= max_delta:
        res = new
    else:
        res = 0.0
    return res


track_len = 10
detect_interval = 5
tracks = []
frame_idx = 0
VIDEO_SCALE = 0.35


###################################################

drone = tellopy.Tello()
container = None


def connectDrone():
    global container
    drone.connect()
    drone.wait_for_connection(60.0)
    container = av.open(drone.get_video_stream())
    getVideo()


###################################################

speed = 100
throttle = 0.0
yaw = 0.0
pitch = 0.0
roll = 0.0


def checkController():
    global buttons
    global speed
    global throttle
    global yaw
    global pitch
    global roll
    global drone

    global forwardLabel
    global backwardLabel
    global upLabel
    global downLabel
    global leftLabel
    global rightLabel
    global clockwiseLabel
    global counterclockwiseLabel
    global pitchLabel
    global yawLabel
    global throttleLabel
    global rollLabel

    for e in pygame.event.get():
        if e.type == pygame.locals.JOYAXISMOTION:
            # ignore small input values (Deadzone)
            if -buttons.DEADZONE <= e.value and e.value <= buttons.DEADZONE:
                e.value = 0.0
            if e.axis == buttons.LEFT_Y:
                throttle = update(
                    throttle, e.value * buttons.LEFT_Y_REVERSE)
                drone.set_throttle(throttle)
                throttleLabel.configure(text="Throttle: " + str("%.2f" % throttle))
                throttleLabel.update()
            if e.axis == buttons.LEFT_X:
                yaw = update(yaw, e.value * buttons.LEFT_X_REVERSE)
                drone.set_yaw(yaw)
                yawLabel.configure(text="Yaw: " + str("%.2f" % yaw))
                yawLabel.update()
            if e.axis == buttons.RIGHT_Y:
                pitch = update(pitch, e.value *
                               buttons.RIGHT_Y_REVERSE)
                drone.set_pitch(pitch)
                pitchLabel.configure(text="Pitch: " + str("%.2f" % pitch))
                pitchLabel.update()
            if e.axis == buttons.RIGHT_X:
                roll = update(roll, e.value * buttons.RIGHT_X_REVERSE)
                drone.set_roll(roll)
                rollLabel.configure(text="Roll: " + str("%.2f" % roll))
                rollLabel.update()

        elif e.type == pygame.locals.JOYHATMOTION:
            if e.value[0] < 0:
                drone.counter_clockwise(speed)
                counterclockwiseLabel.configure(text="Counterclockwise: " + str(speed))
                counterclockwiseLabel.update()
            if e.value[0] == 0:
                drone.clockwise(0)
                clockwiseLabel.configure(text="Clockwise: " + str(0))
                clockwiseLabel.update()
            if e.value[0] > 0:
                drone.clockwise(speed)
                clockwiseLabel.configure(text="Clockwise: " + str(speed))
                clockwiseLabel.update()
            if e.value[1] < 0:
                drone.down(speed)
                downLabel.configure(text="Down: " + str(speed))
                downLabel.update()
            if e.value[1] == 0:
                drone.up(0)
                upLabel.configure(text="Up: " + str(0))
                upLabel.update()
            if e.value[1] > 0:
                drone.up(speed)
                upLabel.configure(text="Up: " + str(speed))
                upLabel.update()
        elif e.type == pygame.locals.JOYBUTTONDOWN:
            if e.button == buttons.LAND:
                drone.land()
            elif e.button == buttons.UP:
                drone.up(speed)
                upLabel.configure(text="Up: " + str(speed))
                upLabel.update()
            elif e.button == buttons.DOWN:
                drone.down(speed)
                downLabel.configure(text="Down: " + str(speed))
                downLabel.update()
            elif e.button == buttons.ROTATE_RIGHT:
                drone.clockwise(speed)
                clockwiseLabel.configure(text="Clockwise: " + str(speed))
                clockwiseLabel.update()
            elif e.button == buttons.ROTATE_LEFT:
                drone.counter_clockwise(speed)
                counterclockwiseLabel.configure(text="Counterclockwise: " + str(speed))
                counterclockwiseLabel.update()
            elif e.button == buttons.FORWARD:
                drone.forward(speed)
                forwardLabel.configure(text="Forward: " + str(speed))
                forwardLabel.update()
            elif e.button == buttons.BACKWARD:
                drone.backward(speed)
                backwardLabel.configure(text="Backward: " + str(speed))
                backwardLabel.update()
            elif e.button == buttons.RIGHT:
                drone.right(speed)
                rightLabel.configure(text="Right: " + str(speed))
                rightLabel.update()
            elif e.button == buttons.LEFT:
                drone.left(speed)
                leftLabel.configure(text="Left: " + str(speed))
                leftLabel.update()
        elif e.type == pygame.locals.JOYBUTTONUP:
            if e.button == buttons.TAKEOFF:
                drone.takeoff()
            elif e.button == buttons.UP:
                drone.up(0)
                upLabel.configure(text="Up: " + str(0))
                upLabel.update()
            elif e.button == buttons.DOWN:
                drone.down(0)
                downLabel.configure(text="Down: " + str(0))
                downLabel.update()
            elif e.button == buttons.ROTATE_RIGHT:
                drone.clockwise(0)
                clockwiseLabel.configure(text="Clockwise: " + str(0))
                clockwiseLabel.update()
            elif e.button == buttons.ROTATE_LEFT:
                drone.counter_clockwise(0)
                counterclockwiseLabel.configure(text="Counterclockwise: " + str(0))
                counterclockwiseLabel.update()
            elif e.button == buttons.FORWARD:
                drone.forward(0)
                forwardLabel.configure(text="Forward: " + str(0))
                forwardLabel.update()
            elif e.button == buttons.BACKWARD:
                drone.backward(0)
                backwardLabel.configure(text="Backward: " + str(0))
                backwardLabel.update()
            elif e.button == buttons.RIGHT:
                drone.right(0)
                rightLabel.configure(text="Right: " + str(0))
                rightLabel.update()
            elif e.button == buttons.LEFT:
                drone.left(0)
                leftLabel.configure(text="Left: " + str(0))
                leftLabel.update()


###################################################
imageTk = None


def getVideo():
    global tracks
    global track_len
    global detect_interval
    global frame_idx
    global VIDEO_SCALE
    global videoLabel
    global typeOfVideo

    try:
        while True:
            time.sleep(0.01)
            for frameRaw in container.decode(video=0):
                checkController()
                frame1 = cv.cvtColor(
                    np.array(frameRaw.to_image()), cv.COLOR_RGB2BGR)
                frame = cv.resize(
                    frame1, (0, 0), fx=VIDEO_SCALE, fy=VIDEO_SCALE)
                frame_gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
                vis = frame.copy()

                if len(tracks) > 0:
                    img0, img1 = prev_gray, frame_gray
                    p0 = np.float32([tr[-1]
                                     for tr in tracks]).reshape(-1, 1, 2)
                    p1, _st, _err = cv.calcOpticalFlowPyrLK(
                        img0, img1, p0, None, **lk_params)
                    p0r, _st, _err = cv.calcOpticalFlowPyrLK(
                        img1, img0, p1, None, **lk_params)
                    d = abs(p0 - p0r).reshape(-1, 2).max(-1)
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
                    cv.polylines(vis, [np.int32(tr)
                                       for tr in tracks], False, (0, 255, 0))
                    draw_str(vis, (20, 20), 'track count: %d' % len(tracks))

                if frame_idx % detect_interval == 0:
                    mask = np.zeros_like(frame_gray)
                    mask[:] = 255
                    for x, y in [np.int32(tr[-1]) for tr in tracks]:
                        cv.circle(mask, (x, y), 5, 0, -1)
                    p = cv.goodFeaturesToTrack(
                        frame_gray, mask=mask, **feature_params)
                    if p is not None:
                        for x, y in np.float32(p).reshape(-1, 2):
                            tracks.append([(x, y)])

                frame_idx += 1
                prev_gray = frame_gray
                #cv.imshow('Tello Dense Optical - Middlebury Research', vis)

                if typeOfVideo.get() == "Optical Flow":
                    im = Image.fromarray(vis, 'RGB')
                    imageTk = ImageTk.PhotoImage(image=im)
                    videoLabel.configure(image=imageTk)
                    videoLabel.image = imageTk
                    videoLabel.update()
                elif typeOfVideo.get() == "Normal":
                    im = Image.fromarray(frame, 'RGB')
                    imageTk = ImageTk.PhotoImage(image=im)
                    videoLabel.configure(image=imageTk)
                    videoLabel.image = imageTk
                    videoLabel.update()

                # mainloop()
                #mainFrame.update()

            ch = cv.waitKey(1)
            if ch == 27:
                break
    except Exception as ex:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        traceback.print_exception(exc_type, exc_value, exc_traceback)
        print(ex)

###################################################

def takeoff():
    global drone
    drone.takeoff()

def land():
    global drone
    drone.land()

def flipForward():
    global drone
    drone.flip_forward()
def flipBackward():
    global drone
    drone.flip_back()
def flipRight():
    global drone
    drone.flip_right()
def flipLeft():
    global drone
    drone.flip_left()
def flipForwardLeft():
    global drone
    drone.flip_forwardleft()
def flipForwardRight():
    global drone
    drone.flip_forwardright()
def flipBackwardLeft():
    global drone
    drone.flip_backleft()
def flipBackwardRight():
    global drone
    drone.flip_backright()

###################################################


try:
    # Set up main frame
    mainFrame = Tk()
    mainFrame.title("Tello: Middlebury Research")

    # Set up and bind trajectory labels
    forwardLabel = Label(mainFrame, text="Forward: 0")
    backwardLabel = Label(mainFrame, text="Backward: 0")
    upLabel = Label(mainFrame, text="Up: 0")
    downLabel = Label(mainFrame, text="Down: 0")
    leftLabel = Label(mainFrame, text="Left: 0")
    rightLabel = Label(mainFrame, text="Right: 0")
    clockwiseLabel = Label(mainFrame, text="Clockwise: 0")
    counterclockwiseLabel = Label(mainFrame, text="Counterclockwise: 0")
    pitchLabel = Label(mainFrame, text="Pitch: 0")
    yawLabel = Label(mainFrame, text="Yaw: 0")
    throttleLabel = Label(mainFrame, text="Throttle: 0")
    rollLabel = Label(mainFrame, text="Roll: 0")

    forwardLabel.grid(row=1, column=1, sticky=E)
    backwardLabel.grid(row=2, column=1, sticky=E)
    upLabel.grid(row=3, column=1, sticky=E)
    downLabel.grid(row=4, column=1, sticky=E)
    leftLabel.grid(row=5, column=1, sticky=E)
    rightLabel.grid(row=6, column=1, sticky=E)
    clockwiseLabel.grid(row=7, column=1, sticky=E)
    counterclockwiseLabel.grid(row=8, column=1, sticky=E)
    pitchLabel.grid(row=9, column=1, sticky=E)
    yawLabel.grid(row=10, column=1, sticky=E)
    throttleLabel.grid(row=11, column=1, sticky=E)
    rollLabel.grid(row=12, column=1, sticky=E)

    # Set up and bind buttons
    connectControllerButton = Button(
        mainFrame, text="Connect Controller", command=connectController)
    connectControllerButton.grid(row=1, column=3, sticky=W)

    connectDroneButton = Button(
        mainFrame, text="Connect Drone", command=connectDrone)
    connectDroneButton.grid(row=2, column=3, sticky=W)

    getVidoButton = Button(mainFrame, text="GetVideo", command=getVideo)
    #getVidoButton.grid(row=13, column=1, sticky=W)

    takeoffButton = Button(mainFrame, text="Takeoff", command=takeoff)
    takeoffButton.grid(row=3, column=3, sticky=W)

    landButton = Button(mainFrame, text="Land", command=land)
    landButton.grid(row=4, column=3, sticky=W)

    # Add flip buttons
    flipForwardButton = Button(mainFrame, text="Flip Forward", command=flipForward)
    flipBackwardButton = Button(mainFrame, text="Flip Backward", command=flipBackward)
    flipRightButton = Button(mainFrame, text="Flip Right", command=flipRight)
    flipLeftButton = Button(mainFrame, text="Flip Left", command=flipLeft)
    flipForwardLeftButton = Button(mainFrame, text="Flip Forward Left", command=flipForwardLeft)
    flipForwardRightButton = Button(mainFrame, text="Flip Forward Right", command=flipForwardRight)
    flipBackwardLeftButton = Button(mainFrame, text="Flip Backward Left", command=flipBackwardLeft)
    flipBackwardRightButton = Button(mainFrame, text="Flip Backward Right", command=flipBackwardRight)

    flipForwardButton.grid(row=5, column=3, sticky=W)
    flipBackwardButton.grid(row=6, column=3, sticky=W)
    flipRightButton.grid(row=7, column=3, sticky=W)
    flipLeftButton.grid(row=8, column=3, sticky=W)
    flipForwardLeftButton.grid(row=9, column=3, sticky=W)
    flipForwardRightButton.grid(row=10, column=3, sticky=W)
    flipBackwardLeftButton.grid(row=11, column=3, sticky=W)
    flipBackwardRightButton.grid(row=12, column=3, sticky=W)

    typeOfVideo = StringVar(mainFrame)
    typeOfVideo.set("Normal") # default value
    w = OptionMenu(mainFrame, typeOfVideo, "Normal", "Optical Flow")
    w.grid(row=0, column=1, columnspan=3, sticky=W+E+N+S)

    img = cv.imread('pic.jpg')
    im = Image.fromarray(img)
    imageTk = ImageTk.PhotoImage(image=im)
    videoLabel = Label(mainFrame, image=imageTk)
    videoLabel.grid(row=1, rowspan=12, column=2, sticky=N)

    mainloop()

except Exception as ex:
    exc_type, exc_value, exc_traceback = sys.exc_info()
    traceback.print_exception(exc_type, exc_value, exc_traceback)
    print(ex)
finally:
    drone.quit()
    cv.destroyAllWindows()
