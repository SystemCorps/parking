import serial as ser
import os
import time
from multiprocessing import Process, Value, Array, Queue
from multiprocessing.managers import BaseManager
from queue import LifoQueue
import cv2

from imutils.video import FPS


def WheelSpeed(lifo):
    rec = ser.Serial("/dev/tty.SLAB_USBtoUART", 921600)
    imud = [0]*4
    while(1):
        res = rec.readline()
        #100 - 1, 0.1, 0.1, 0.2, 43\r\n
        splited = res.split(b',')

        imud[0] = float(splited[1])
        imud[1] = float(splited[2])
        imud[2] = float(splited[3])
        imud[3] = float(splited[4][0:-2])

        #print(xdps, ydps, zdps, bat)
        lifo.put(imud)

    rec.close()

"""
def test(q):
    testing = 1
    while(True):

        testing = testing+1
        time.sleep(0.01)
        print(testing)
        q.put(testing)
"""

class MyManager(BaseManager):
    pass
MyManager.register('LifoQueue', LifoQueue)


if __name__ == '__main__':

    # Set camera
    cap = cv2.VideoCapture(0)
    # Set IMU sensor
    #rec = ser.Serial("/dev/tty.SLAB_USBtoUART", 921600)
    # For calculating FPS
    prevTime = 0


    manager = MyManager()
    manager.start()
    lifo = manager.LifoQueue()

    # For IMU data reading (multiprocess)
    proc = Process(target=WheelSpeed, args=[lifo, ])
    proc.start()


    #testp = Process(target=test, args=[lifo, ])
    #testp.start()
    # Video capture & IMU reading loop
    while(True):
        # Read image
        ret, frame = cap.read()

        # For FPS
        curTime = time.time()
        sec = curTime - prevTime
        prevTime = curTime
        fps = 1/sec

        # Read IMU data
        #res = rec.readline()

        # Print FPS and IMU data
        #print(fps, xdps)


        print(fps)
        fromq1 = lifo.get()
        #fromq2 = lifo.get()
        print("From queue: ",fromq1)

        # Show video stream
        cv2.imshow('frame', frame)
        # Finishing loop when 'q' pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    #rec.close()

    # Close IMU process
    proc.terminate()
    #testp.terminate()
    """
    proc = Process(target=WheelSpeed, args=[])
    proc.start()
    proc.terminate()
    """