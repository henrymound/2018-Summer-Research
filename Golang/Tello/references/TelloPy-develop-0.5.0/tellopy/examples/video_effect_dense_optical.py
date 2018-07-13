import sys
import traceback
import tellopy
import av
import cv2.cv2 as cv2  # for avoidance of pylint error
import numpy as np


def main():
    drone = tellopy.Tello()

    try:
        drone.connect()
        drone.wait_for_connection(60.0)

        container = av.open(drone.get_video_stream())
        frameCount = 0 # Stores the current frame being processed
        frame1 = None # Store variables for first frame
        frame2 = None # Store variables for second frame
        prvs = None
        hsv = None

        while True:
            for frame in container.decode(video=0):
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
