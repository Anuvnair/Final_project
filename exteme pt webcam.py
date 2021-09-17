import cv2
import numpy as np
import math

#This program uses the webcam of the laptop and identifies the finger tips of the hand

cap = cv2.VideoCapture(0)

#variables that are used later in the program
count_defects=0 #number of convexity defects that are considered from all the defects that are identified 
dist_max_i=0
indexes=0
while True:
    ret, img = cap.read()

    #crop_image is the region of interest. The part of the 'img' captured from cap.read() that detects finger tips
    cv2.rectangle(img,(300,300),(100,100),(0,255,0),0)
    crop_img=img[100:300,100:300]

    #coverting to gray-scale and blurring to remove noise
    grey = cv2.cvtColor(crop_img, cv2.COLOR_BGR2GRAY)
    value=(7,7)
    blurred = cv2.GaussianBlur(grey, value, 0)

    #thresholding the image
    _, thresh1 = cv2.threshold(blurred, 127, 255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)


    #finding contours
    _, contours, hierarchy = cv2.findContours(thresh1.copy(),cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    cnt = max(contours, key = lambda x: cv2.contourArea(x))

    #calculating the centroid(this is for further enhancement - to identify only the farthest defects. )
    M = cv2.moments(cnt)
    cx = int(M['m10']/M['m00'])
    cy = int(M['m01']/M['m00'])
    cv2.circle(crop_img,(cx,cy),3,[0,0,255],3)


    #drawing a rectangle over the biggest contour (sorted by area)
    x,y,w,h = cv2.boundingRect(cnt)
    cv2.rectangle(crop_img,(x,y),(x+w,y+h),(0,0,255),0)

    #convexity hull is drawn 
    hull = cv2.convexHull(cnt)
    drawing = np.zeros(crop_img.shape,np.uint8)
    cv2.drawContours(drawing,[cnt],0,(0,255,0),0)
    cv2.drawContours(drawing,[hull],0,(0,0,255),0)

    #determining the defects
    hull = cv2.convexHull(cnt,returnPoints = False)
    defects = cv2.convexityDefects(cnt,hull)

    for i in range(defects.shape[0]):
        s,e,f,_ = defects[i,0]
        start = tuple(cnt[s][0])
        end = tuple(cnt[e][0])
        far = tuple(cnt[f][0])

        #eliminating the defect points that are not the needed 

        a = math.sqrt((end[0] - start[0])**2 + (end[1] - start[1])**2)
        b = math.sqrt((far[0] - start[0])**2 + (far[1] - start[1])**2)
        c = math.sqrt((end[0] - far[0])**2 + (end[1] - far[1])**2)
        angle = math.acos((b**2 + c**2 - a**2)/(2*b*c)) * 57
        if angle <= 90:
            count_defects += 1
            cv2.circle(crop_img,start,3,[0,0,255],2)



    cv2.imshow('finger tips', img)

    k = cv2.waitKey(10)
    if k == 27:
        break

cap.release()
cv2.destroyAllWindows()
