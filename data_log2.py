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


def imgSave(lifo):


    while(1):
        if lifo.empty() == False:
            img_cnt, img, vel = lifo.get()
            filedir = "/Users/astra/Documents/parking_img/img%d~%.1f.png" % (img_cnt, vel)
            cv2.imwrite(filename=filedir, img=img)





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
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter("/Users/astra/Documents/parking_img/test.avi", fourcc, 30, (640,360))

    # For calculating FPS
    prevTime = 0


    manager = MyManager()
    manager.start()
    lifo = manager.LifoQueue()

    # For data saving
    slifo = manager.LifoQueue()

    # For IMU data reading (multiprocess)
    proc = Process(target=WheelSpeed, args=[lifo, ])
    proc.start()

    #sproc = Process(target=imgSave, args=[slifo, ])
    #sproc.start()
    #testp = Process(target=test, args=[lifo, ])
    #testp.start()
    # Video capture & IMU reading loop
    img_cnt = 0
    while(cap.isOpened()):
        # Read image
        ret, frame = cap.read()

        out.write(frame)


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

        #slifo.put([img_cnt, frame, fromq1[0]])
        img_cnt=img_cnt+1
        # Finishing loop when 'q' pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    #rec.close()

    # Close IMU process
    proc.terminate()
    #sproc.terminate()
    #testp.terminate()

    """
    while(slifo.empty()==False):
        cnt, img, vel = slifo.get()
        filedir = "/Users/astra/Documents/parking_img/img%d~%.1f.png" % (cnt, vel)
        cv2.imwrite(filename=filedir, img=img)
    """

    """
    proc = Process(target=WheelSpeed, args=[])
    proc.start()
    proc.terminate()
    """