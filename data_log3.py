import serial as ser
import os
import time
from multiprocessing import Process, Value, Array, Queue
from multiprocessing.managers import BaseManager
from queue import LifoQueue
import cv2


class MyManager(BaseManager):
    pass
MyManager.register('LifoQueue', LifoQueue)


if __name__ == '__main__':

    # Set camera


    manager = MyManager()
    manager.start()
    lifo = manager.LifoQueue()

    img = cv2.imread("/Users/astra/Downloads/59308.jpg")
    lifo.put([img, 20])


    a, b = lifo.get()
    cv2.imshow("Test",a)
    #b = lifo.get()
    print(b)

    cv2.waitKey(0)
    cv2.destroyAllWindows()