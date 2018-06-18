import sys
import traceback
import tellopy
import av
import cv2.cv2 as cv  # for avoidance of pylint error
import numpy as np
#import video
from common import anorm2, draw_str
from time import clock


def main():
    drone = tellopy.Tello()

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

        track_len = 10
        detect_interval = 5
        tracks = []
        frame_idx = 0

        #drone.set_video_encoder_rate(2)
        container = av.open(drone.get_video_stream())

        while True:
            for frameRaw in container.decode(video=0):
                frame1 = cv.cvtColor(np.array(frameRaw.to_image()), cv.COLOR_RGB2BGR)
                frame = cv.resize(frame1, (0,0), fx=0.5, fy=0.5)
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
