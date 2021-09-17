from picamera.array import PiRGBArray   #PiRGBArray helps convertng image into rgb matrix to help in mathematical calculation
from picamera import PiCamera           #for initialising picamera
import time                             #for delay
import cv2                              #for image processing
import numpy as np                      #for calculations ease
import RPi.GPIO as GPIO                 #to acces rpi pins

GPIO.setmode(GPIO.BOARD)                #naming the rpi pins(other option is GPIO.BCM)
GPIO.setwarnings(False)                 #to suppress warning which occurs when same rpi pin is accesed twice
GPIO.setup(8,GPIO.OUT)                  #setting pin 8 as output
GPIO.setup(10,GPIO.OUT)                 #setting pin 10 as output

camera = PiCamera()                     #initialising picamera
camera.resolution = (640, 480)          #setting camera resolution as 640 width and 480 height
camera.framerate = 32                   #32 frames per second
rawCapture = PiRGBArray(camera, size=(640, 480))#putting the settings into PiRGBArray
  
time.sleep(0.1)                         #delay time for picamera to warmup

#lower = np.array([0,60,80])            #HSV lower range values for skin colour
#upper = np.array([20,140,250])         #HSV upper range values for skin colour

lower = np.array([0,80,90])
upper = np.array([30,160,210])

GPIO.output(8,False)                    #setting pin8 as low
GPIO.output(10,False)                   #setting pin 10 as low

print 'please adjust your hand inframe of the camera' #displays in screen
i=0                                     #intialising i to 0
for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):#starting for loop for picamera, captures image in bgr format
   try:                                 #try method is used so that any exceptions raised, during code execution donot break the loop
        image = frame.array             #puts the frame captured in variable image
    
        hsv = cv2.cvtColor(image,cv2.COLOR_BGR2HSV)#converts bgr image to hsv colour space
   
        mask = cv2.inRange(hsv,lower,upper)    #create a mask using the gven hsv range
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(5,5)) #create a structuring element of matrix 5,5
        dil = cv2.dilate(mask, kernel, iterations=1)  # dilate the mask one time using the created kernel

        im2, contours, hierarchy = cv2.findContours(dil,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)#find the edge pixel (x,y) values of all     skin                                                                                           coloured objects in the frame
        cnt = max(contours, key = cv2.contourArea)  #find the object with the largest area, assumed to be the hand

        x,y,w,h = cv2.boundingRect(cnt)             #obtain the starting (x,y) position of the object, its height and width
        cv2.rectangle(image,(x,y),(x+w,y+h),(0,255,0),2) # draw a rectangle around the object in green colour with thickness 2
        print h,w                                   #print the height and widht
        if i==0:                                  
               # if w in range(140,170) and h in range (230,260):
                if h in range (240,280) and w in range(110,150):  #this is the position the hand must be in , to continue with the recogntion                                                          part
                        print 'in frmae'
                        print 'pls use this frame position. any change can lead to errors in output'
                        time.sleep(2)
                        i=i+1
                else:
                        print 'out of frame'                # else show that the hand is not in reference plane
        else:
                #if h in range(230,260) and w in range(140,170):
                if h in range (240,280) and w in range(110,150):
                        print 'gesture1'
                        #GPIO.output(8,True)
                        #GPIO.output(10,False)
                #elif h in range(230,260) and w in range(250,270):
                elif h in range(240,280) and w in range(230,270):
                        print 'gesture2'
                        #GPIO.output(8,False)
                        #GPIO.output(10,True)
                elif h in range(145,195) and w in range(120,150):
                        print 'gesture3'
                        #GPIO.output(8,True)
                        #GPIO.output(10,True)
                elif h in range(205,235) and w in range(105,135):
                        print 'gesture4'
                        #GPIO.output(8,False)
                        #GPIO.output(10,False)
                elif h in range(235,265) and w in range(115,145):
                        print 'gesture5'
                else:
                        print 'unknown gesture'

        cv2.imshow('blah',image)            # show the frame
        #cv2.imshow("Frame",image)
        key = cv2.waitKey(1) & 0xFF         
 
        rawCapture.truncate(0)              #commands the picamera to release the frame, then only camera can capture a new frame
 
  
        if key == ord("q"):                 #if 'q' key is pressed in keyboard the program stops
                break
   except ValueError:                       #if no skin colour object is detected in the frame, ValueError exception is raised because opencv                                       cannot find the largest object when everything is 0
           print 'no object'
           rawCapture.truncate(0)           #in such case, camera release the frame , print 'no object' and continue for next pass in loop
           pass
