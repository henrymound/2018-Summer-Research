from tkinter import *
import sys
import traceback
import tellopy
import av
import cv2.cv2 as cv2  # for avoidance of pylint error
import numpy
import _thread
import time

root = Tk()
root.title("Tello Swarm")

#wifiInterface
wifiInterfaceLabel = Label(root, text="Wifi Interface: ")
wifiInterfaceLabel.grid(row=1, column=0, sticky=E)
wifiInterfaceText = Text(root, height=1, width=10)
wifiInterfaceText.grid(row=1, column=1, sticky=W)
wifiInterfaceText.insert(END, "wlp1s0")

#port
portLabel = Label(root, text="Port: ")
portLabel.grid(row=2, column=0, sticky=E)
portText = Text(root, height=1, width=10)
portText.grid(row=2, column=1, sticky=W)
portText.insert(END, "9000")

#videoPort
videoPortLabel = Label(root, text="Video Port: ")
videoPortLabel.grid(row=3, column=0, sticky=E)
videoPortText = Text(root, height=1, width=10)
videoPortText.grid(row=3, column=1, sticky=W)
videoPortText.insert(END, "6038")

#connReqPort
connectionRequestPortLabel = Label(root, text="ConnRequest Port: ")
connectionRequestPortLabel.grid(row=4, column=0, sticky=E)
connectionRequestPortText = Text(root, height=1, width=10)
connectionRequestPortText.grid(row=4, column=1, sticky=W)
connectionRequestPortText.insert(END, "9617")

def connectDrone1():
    global videoPortText
    global connectionRequestPortText
    global portText
    global wifiInterfaceText

    videoPort = int(videoPortText.get("1.0", END).strip())
    port = int(portText.get("1.0", END).strip())
    wifiInterface = wifiInterfaceText.get("1.0", END).strip()
    connectionRequest = int(connectionRequestPortText.get("1.0", END).strip())

    print(videoPort)
    print(port)
    print(wifiInterface)
    print(connectionRequest)

    drone = tellopy.Tello(wifiInterface, port, videoPort, connectionRequest)

    try:
        drone.connect()
        drone.wait_for_connection(60.0)
        container = av.open(drone.get_video_stream())
        while True:
            for frame in container.decode(video=0):
                image = cv2.cvtColor(numpy.array(frame.to_image()), cv2.COLOR_RGB2BGR)
                cv2.imshow('Drone', image)
                cv2.waitKey(1)

    except Exception as ex:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        traceback.print_exception(exc_type, exc_value, exc_traceback)
        print(ex)
    finally:
        drone.quit()
        cv2.destroyAllWindows()


def connectDrone2():
    global videoPortText
    global connectionRequestPortText
    global portText
    global wifiInterfaceText

    videoPort = int(videoPortText.get("1.0", END).strip())
    port = int(portText.get("1.0", END).strip())
    wifiInterface = wifiInterfaceText.get("1.0", END).strip()
    connectionRequest = int(connectionRequestPortText.get("1.0", END).strip())

    print(videoPort)
    print(port)
    print(wifiInterface)
    print(connectionRequest)

    drone2 = tellopy.Tello(wifiInterface, port, videoPort, connectionRequest)

    try:
        drone2.connect()
        drone2.wait_for_connection(60.0)
        container2 = av.open(drone2.get_video_stream())
        while True:
            for frame in container2.decode(video=0):
                image = cv2.cvtColor(numpy.array(frame.to_image()), cv2.COLOR_RGB2BGR)
                cv2.imshow('Drone', image)
                cv2.waitKey(1)

    except Exception as ex:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        traceback.print_exception(exc_type, exc_value, exc_traceback)
        print(ex)
    finally:
        drone2.quit()
        cv2.destroyAllWindows()

def connectDrone1Thread():
    _thread.start_new_thread(connectDrone1, ())
def connectDrone2Thread():
    _thread.start_new_thread(connectDrone2, ())


#connectButtons
connectButton1 = Button(root, text="Connect Drone 1", command=connectDrone1Thread)
connectButton1.grid(row=5, column=0, columnspan=1, sticky=N)
connectButton2 = Button(root, text="Connect Drone 2", command=connectDrone2Thread)
connectButton2.grid(row=5, column=1, columnspan=1, sticky=N)
mainloop()
