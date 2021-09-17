from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2
import numpy as np
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
GPIO.setup(31,GPIO.OUT)
GPIO.setup(33,GPIO.OUT)
GPIO.setup(35,GPIO.OUT)
GPIO.setup(37,GPIO.OUT)

camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 32
rawCapture = PiRGBArray(camera, size=(640, 480))
 
time.sleep(0.1)

#lower = np.array([0,60,80])
#upper = np.array([20,140,250])

lower = np.array([0,80,90])
upper = np.array([30,160,210])

GPIO.output(31,True)
GPIO.output(33,True)
GPIO.output(35,True)
GPIO.output(37,True)
count1 = 0
count2 = 0
count3 = 0
count4 = 0
flag1 = 0
flag2 = 0
flag3 = 0
flag4 = 0

print 'please adjust your hand inframe of the camera'
i=0
for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
   try:
        image = frame.array
   
        hsv = cv2.cvtColor(image,cv2.COLOR_BGR2HSV)
   
        mask = cv2.inRange(hsv,lower,upper)
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(5,5))
        dil = cv2.dilate(mask, kernel, iterations=1)

        im2, contours, hierarchy = cv2.findContours(dil,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
        cnt = max(contours, key = cv2.contourArea)

        x,y,w,h = cv2.boundingRect(cnt)
        cv2.rectangle(image,(x,y),(x+w,y+h),(0,255,0),2)
        print h,w
        if i==0:
               # if w in range(140,170) and h in range (230,260):
                if h in range (240,280) and w in range(110,150):
                        print 'in frame'
                        print 'pls use this frame position. any change can lead to errors in output'
                        time.sleep(2)
                        i=i+1
                else:
                        print 'out of frame'
        else:
                #if h in range(230,260) and w in range(140,170):
                if h in range (240,280) and w in range(110,150):
                        print 'gesture1'
                        count1 += 1
                        count2 = 0
                        count3 = 0
                        count4 = 0
                        if count1 >5:
                           if flag1 == 0:
                              print 'device 1 on'
                              flag1 = 1
                              count1 = 0
                              GPIO.output(31,False)
                              time.sleep(1)   
                           else:
                              print 'device 1 off'
                              flag1 = 0
                              count1 = 0
                              GPIO.output(31,True)
                              time.sleep(1)
                #elif h in range(230,260) and w in range(250,270):
                elif h in range(240,280) and w in range(230,270):
                        print 'gesture2'
                        count1 = 0
                        count2 += 1
                        count3 = 0
                        count4 = 0
                        if count2 > 5:
                           if flag2 == 0:
                              print 'device 2 on'
                              flag2 = 1
                              count2 = 0
                              GPIO.output(33,False)
                              time.sleep(1)
                           else:
                              print ' device 2 off'
                              flag2 = 0
                              count2 = 0
                              GPIO.output(33,True)
                              time.sleep(1)
                #elif h in range(145,195) and w in range(120,150):
                elif h in range(120,160) and w in range(130,170):
                        print 'gesture3'
                        count1 = 0
                        count2 = 0
                        count3 += 1
                        count4 = 0
                        if count3 > 5:
                           if flag3 == 0:
                              print'device 3 on'
                              flag3 = 1
                              count3 = 0
                              GPIO.output(35,False)
                              time.sleep(1)
                           else:
                              print 'device 3 off'
                              flag3 = 0
                              count3 = 0
                              GPIO.output(35,True)
                              time.sleep(1)
                #elif h in range(205,235) and w in range(105,135):
                elif h in range(200,240) and w in range(80,120):
                        print 'gesture4'
                        count1 = 0 
                        count2 = 0
                        count3 = 0
                        count4 += 1
                        if count4 > 5:
                           if flag4 == 0:
                              print 'device4 on'
                              flag4 = 1
                              count4 = 0
                              GPIO.output(37,False)
                              time.sleep(1)
                           else:
                              print ' device 4 off'
                              flag4 = 0
                              count4 = 0
                              GPIO.output(37,True)
                              time.sleep(1)
                else:
                        print 'unknown gesture'
                        count1 = 0
                        count2 = 0
                        count3 = 0
                        count4 = 0

        cv2.imshow('blah',image)
        #cv2.imshow("Frame",image)
        key = cv2.waitKey(1) & 0xFF
 
        rawCapture.truncate(0)
 
  
        if key == ord("q"):
           GPIO.output(31,True)
           GPIO.output(33,True)
           GPIO.output(35,True)
           GPIO.output(37,True)
           break
   except ValueError:
           print 'no object'
           rawCapture.truncate(0)
           pass
