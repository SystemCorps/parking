import serial as ser
import os
import time
from multiprocessing import Process, Value, Array

import cv2

from imutils.video import FPS


#global res
global xdps, ydps, zdps, bat

def WheelSpeed():
    rec = ser.Serial("/dev/tty.SLAB_USBtoUART", 921600)
    global xdps, ydps, zdps, bat
    while(1):
        res = rec.readline()
        #100 - 1, 0.1, 0.1, 0.2, 43\r\n
        splited = res.split(b',')

        xdps = float(splited[1])
        ydps = float(splited[2])
        zdps = float(splited[3])
        bat = float(splited[4][0:-2])

        #print(xdps, ydps, zdps, bat)

    rec.close()




if __name__ == '__main__':

    # Set camera
    cap = cv2.VideoCapture(0)
    # Set IMU sensor
    #rec = ser.Serial("/dev/tty.SLAB_USBtoUART", 921600)
    # For calculating FPS
    prevTime = 0

    # For IMU data reading (multiprocess)
    proc = Process(target=WheelSpeed, args=[])
    proc.start()

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

    """
    proc = Process(target=WheelSpeed, args=[])
    proc.start()
    proc.terminate()
    """