import picamera
from picamera.array import PiRGBArray 
import cv,cv2
import time
import numpy as np

try:
    with picamera.PiCamera() as camera:
        camera.rotation = 0
        camera.resolution = (640,480)
        rawCapture = PiRGBArray(camera,size=(640,480))
        fx = open('X','w')
        fx.write("320")
        fy = open('Y','w')
        fy.write("240")
        for frame in camera.capture_continuous(rawCapture,format = "bgr", use_video_port=True):

            imgOriginal = frame.array #similiar to Mat original
            imgHSV = cv2.cvtColor(imgOriginal,cv2.COLOR_BGR2HSV)
            #imgThreshold =cv2.inRange(imgHSV,cv.Scalar(0,150,0),cv.Scalar(10,255,100))# deep red
            #imgThreshold =cv2.inRange(imgHSV,cv.Scalar(15,50,160),cv.Scalar(20,255,255))#pinponball
            imgThreshold =cv2.inRange(imgHSV,cv.Scalar(170,100,100),cv.Scalar(180,255,255))#light red
            # Hue Sat Value
            #Sat smaller more white
            #Value smaller more black
            #bightness Red H 170-180  S 100-255 V 100-255
            #Red  H 0-10  S 150-255   V  0-100
            #pinponball  H 15-20   S 50-255  V 160-255
            M = cv2.moments(imgThreshold)
            if M['m00'] > 50000 :
                mx = int(M['m10']/M['m00']) # mx center = 320
                my = int(M['m01']/M['m00']) # my center = 240
                fx = open('X','w')
                fx.write(str(mx))
                fy = open('Y','w')
                fy.write(str(my))
                """
		print "Area = ",M['m00'],"x = ",mx," , y = ",my
                if mx >=0 and my >=0:
                    cv2.line(imgOriginal,(mx,my),(mx,my),(0,255,0),5)
		"""
            else:
                fx = open('X','w')
                fx.write("320")
                fy = open('Y','w')
                fy.write("240")
                #print "Area = 0"

            #cv2.imshow("Frame",imgOriginal)
            #cv2.imshow("HSV",imgHSV)
            #cv2.imshow("Threshold",imgThreshold)
            key = cv2.waitKey(1) & 0xFF
            rawCapture.truncate(0)
            if key == ord("q"):
                break
except KeyboardInterrupt:
    camera.close()
    cv2.destroyAllWindows()
camera.close()
cv2.destroyAllWindows()
