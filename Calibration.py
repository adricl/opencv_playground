#This code takes images and calibrates the camera based of the images
#we expect the object to be detected in the bottom middle of the cameras view. This will calibrate on the largest object
#in this view

import cv2
import numpy as np
import os
import sys

myDebug = False




def nothing(x):
    pass


###################################################################################################
def calibration(*file):

    cv2.namedWindow('image')
    cv2.createTrackbar('LowH', 'image', 1, 255, nothing)
    cv2.createTrackbar('HighH', 'image', 1, 255, nothing)
    cv2.createTrackbar('LowS', 'image', 1, 255, nothing)
    cv2.createTrackbar('HighS', 'image', 1, 255, nothing)
    cv2.createTrackbar('LowV', 'image', 1, 255, nothing)
    cv2.createTrackbar('HighV', 'image', 1, 255, nothing)
    cv2.namedWindow("imgOriginal", cv2.WINDOW_AUTOSIZE)  # create windows, use WINDOW_AUTOSIZE for a fixed window size
    cv2.namedWindow("imgMorph", cv2.WINDOW_AUTOSIZE)

    if not file:
        imgOriginal = cv2.imread('Pics/aaa.jpg', 1)
    else:
        imgOriginal = cv2.imread(file[0],1)

    imgOriginal = cv2.resize(imgOriginal, (320,240))

    result = list()
    rangeHSV = list()
    if(myDebug):
        rangeHSV.append((0))        
    else:
        rangeHSV = scanImage()
    
    print "Checking Image \n"
#    while(cv2.waitKey(1) != 27):

    while (len(rangeHSV) > 0):

        if (not (myDebug)):
            (lowHSV, highHSV) = rangeHSV.pop()
        else:
            cv2.waitKey(1)
            LowH = cv2.getTrackbarPos('LowH', 'image')
            HighH = cv2.getTrackbarPos('HighH', 'image')
            LowS = cv2.getTrackbarPos('LowS', 'image')
            HighS = cv2.getTrackbarPos('HighS', 'image')
            LowV = cv2.getTrackbarPos('LowV', 'image')
            HighV = cv2.getTrackbarPos('HighV', 'image')
            lowHSV = np.array([LowH, LowS, LowV])
            highHSV = np.array([HighH, HighS, HighV])

        #        imgThresh = cv2.inRange(imgHSV, np.array([153, 29, 106]), np.array([184, 70, 255])) #Pink Ball
        #        imgThresh = cv2.inRange(imgHSV, np.array([168, 119, 63]), np.array([180, 255, 197])) #Red Ball Daylight
        #        imgThresh = cv2.inRange(imgHSV, np.array([154, 255, 37]), np.array([190, 255, 255])) #Red ball night
        #        imgThresh = cv2.inRange(imgHSV, np.array([78, 128, 0]), np.array([141, 255, 255]))
       
        morph = filterImage(imgOriginal, lowHSV, highHSV)
        
        imgCircle, count, maxRadius = circleDetectedBound(morph, imgOriginal)

        #Save the best results
        if (count > 0):
            elems = cv2.countNonZero(morph)
            result.append((imgCircle, count, maxRadius, elems, lowHSV, highHSV))
            #print count, maxRadius, elems, lowHSV, highHSV
        
        if(myDebug):
            cv2.imshow("imgOriginal", imgCircle)  # show windows
            cv2.imshow("imgMorph", morph)

    # end while
    (lowHSVResult, highHSVResult) = sortResults(result)

   
    #cv2.destroyAllWindows()                     # remove windows from memory
    #print (lowHSVResult, highHSVResult)
    return (lowHSVResult, highHSVResult)

###################################################################################################
##We optimise for low element count large radius and low count 
def sortResults(results):
    print "Sorting Results\n"
    results.sort(key=lambda row:row[2])
    results.sort(key=lambda row:row[3], reverse=True)
    count = 0
    f = open('hsvVals.txt', 'w')
    f.write('CircleCount, maxRadius, elemCount, lowHSV, highHSV\n')
    # We take the top 2 results, we really tak the top result for calibration
    for obj in results[:2]:
        f.write(str(obj[1]) + ', ' + str(obj[2]) + ', ' + str(obj[3]) + ', ' + str(obj[4]) + ', ' + str(obj[5]) + '\n')
        cv2.imwrite(str(count) + ".png", obj[0])

        count +=1
    return ((results[0])[4], (results[0])[5])

###################################################################################################
#Give us a range of vaules with which to determine the best HSV value set
########horrible function that must be rewritten 
def scanImage():
    rangeHSV = list()
    print "Generating HSV Ranges \n"
    for i in range(1, 255, 50):
        for j in range(1,255, 50):
            for k in range (1,255, 50):
                for l in range (255, 1,-50):
                    if (i>l): break
                    for m in range (255,1,-50):
                        if (j>m): break
                        for n in range (255,1,-50):
                            if (k>n): break
                            rangeHSV.append((np.array([i, j, k]),np.array([l, m, n])))
        

    return rangeHSV
    
###################################################################################################
def filterImage(imgOriginal, lowHSV, highHSV):
    imgHSV = cv2.cvtColor(imgOriginal, cv2.COLOR_BGR2HSV)
    imgThresh = cv2.inRange(imgHSV,lowHSV, highHSV)

    imgDial = cv2.dilate(imgThresh, np.ones((5, 5), np.uint8))
    imgErode = cv2.erode(imgDial, np.ones((5, 5), np.uint8))

    str_el = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
    morph = cv2.morphologyEx(imgThresh, cv2.MORPH_OPEN, str_el)
    morph = cv2.morphologyEx(morph, cv2.MORPH_CLOSE, str_el)
    return morph

###################################################################################################
def circleDetectedBound(image, imgOriginal):
	height, width, temp = imgOriginal.shape
	xTop = .25 * width #Boudning box for middle bottom of the image to find ball
	yTop = .5 * height
	xBottom = .75 * width
	yBottom = height
	cont, contours, hierarchy = cv2.findContours(image, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
	#contours.sort()
        circleImg = cv2.copyMakeBorder(imgOriginal,0,0,0,0,cv2.BORDER_REPLICATE) #copy image to display Circles

        circleCount = 0
        maxRadius = 0
        cv2.rectangle(circleImg, (int(xTop),int(yTop)), (int(xBottom), int(yBottom)), (0,255,0), 3)
	for i in range(len(contours)):
		(x, y), r = cv2.minEnclosingCircle(contours[i])
		if (xTop <= x and x <= xBottom and yTop <= y and y <= yBottom): 
		    cv2.circle(circleImg, (int(x), int(y)), int(r), (0, 0, 255), 3)
                    circleCount +=1
                    maxRadius = max(maxRadius, r)
                else:
                    return circleImg, 0, 0
		#intRows, intColumns = imgErode.shape
	return circleImg, circleCount, maxRadius


if __name__ == "__main__":
    calibration()
