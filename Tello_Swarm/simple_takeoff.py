from time import sleep
import tellopy


def handler(event, sender, data, **args):
    drone1 = sender
    drone2 = sender
    if event is drone1.EVENT_FLIGHT_DATA:
        print(data)
    if event is drone2.EVENT_FLIGHT_DATA:
        print(data)


def test():
    drone1 = tellopy.Tello("wlxf8788c004f09")
    drone2 = tellopy.Tello("wlp1s0")
    try:
        drone1.subscribe(drone1.EVENT_FLIGHT_DATA, handler)
        drone2.subscribe(drone2.EVENT_FLIGHT_DATA, handler)
        drone1.connect()
        drone2.connect()
        drone1.wait_for_connection(60.0)
        drone2.wait_for_connection(60.0)
        drone1.takeoff()
        drone2.takeoff()
        sleep(5)
        drone1.down(50)
        drone2.down(50)
        sleep(5)
        drone1.land()
        drone2.land()
        sleep(5)
    except Exception as ex:
        print(ex)
    finally:
        drone1.quit()
        drone2.quit()

if __name__ == '__main__':
    test()
