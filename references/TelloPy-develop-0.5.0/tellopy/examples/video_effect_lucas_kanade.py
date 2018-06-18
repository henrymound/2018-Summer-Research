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
        cap = drone.get_video_stream()

        # params for ShiTomasi corner detection
        feature_params = dict( maxCorners = 100,
                               qualityLevel = 0.3,
                               minDistance = 7,
                               blockSize = 7 )

        # Parameters for lucas kanade optical flow
        lk_params = dict( winSize  = (15,15),
                          maxLevel = 2,
                          criteria = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03))
        # Create some random colors
        color = np.random.randint(0,255,(100,3))



        while True:
            for frame in container.decode(video=0):
                old_frame = cv2.cvtColor(np.array(frame.to_image()), cv2.COLOR_RGB2BGR)
                old_gray = cv2.cvtColor(old_frame, cv2.COLOR_BGR2GRAY)
                p0 = cv2.goodFeaturesToTrack(old_gray, mask = None, **feature_params)
                mask = np.zeros_like(old_frame)

                frame = cv2.cvtColor(np.array(frame.to_image()), cv2.COLOR_RGB2BGR)
                frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                # calculate optical flow
                p1, st, err = cv2.calcOpticalFlowPyrLK(old_gray, frame_gray, p0, None, **lk_params)
                # Select good points
                good_new = p1[st==1]
                good_old = p0[st==1]
                # draw the tracks
                for i,(new,old) in enumerate(zip(good_new,good_old)):
                    a,b = new.ravel()
                    c,d = old.ravel()
                    mask = cv2.line(mask, (a,b),(c,d), color[i].tolist(), 2)
                    frame = cv2.circle(frame,(a,b),5,color[i].tolist(),-1)
                img = cv2.add(frame,mask)
                cv2.imshow('frame',img)
                k = cv2.waitKey(30) & 0xff
                if k == 27:
                    break
                # Now update the previous frame and previous points
                old_gray = frame_gray.copy()
                p0 = good_new.reshape(-1,1,2)

                #image = cv2.cvtColor(np.array(frame.to_image()), cv2.COLOR_RGB2BGR)
                #cv2.imshow('Canny', cv2.Canny(image, 100, 200))
                cv2.waitKey(1)

    except Exception as ex:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        traceback.print_exception(exc_type, exc_value, exc_traceback)
        print(ex)
    finally:
        drone.quit()
        cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
