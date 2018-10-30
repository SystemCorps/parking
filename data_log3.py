import serial as ser
import os
import time
import cv2

from imutils.video import FPS
# Set camera
cap = cv2.VideoCapture(0)
# Set IMU sensor
rec = ser.Serial("/dev/tty.SLAB_USBtoUART", 921600)
imud = [0]*4



# For calculating FPS
prevTime = 0


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
    res = rec.readline()
    # 100 - 1, 0.1, 0.1, 0.2, 43\r\n
    splited = res.split(b',')

    imud[0] = float(splited[1])
    imud[1] = float(splited[2])
    imud[2] = float(splited[3])
    imud[3] = float(splited[4][0:-2])
    # Print FPS and IMU data
    #print(fps, xdps)


    print(fps)
    print("IMU: ", imud)

    # Show video stream
    cv2.imshow('frame', frame)
    # Finishing loop when 'q' pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
rec.close()
