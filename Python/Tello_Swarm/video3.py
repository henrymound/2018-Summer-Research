import sys
import traceback
import tellopy
import av
import cv2.cv2 as cv2  # for avoidance of pylint error
import numpy


def main():
    drone2 = tellopy.Tello("wlp1s0", 9000, 6038, 9617)

    try:
        drone2.connect()

        drone2.wait_for_connection(60.0)

        container2 = av.open(drone2.get_video_stream())
        while True:
            for frame in container2.decode(video=0):
                image = cv2.cvtColor(numpy.array(frame.to_image()), cv2.COLOR_RGB2BGR)
                cv2.imshow('Drone 2', image)
                cv2.waitKey(1)

    except Exception as ex:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        traceback.print_exception(exc_type, exc_value, exc_traceback)
        print(ex)
    finally:
        drone2.quit()
        cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
