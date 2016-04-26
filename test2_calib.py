# OpenCV_test_3.py

# this program tracks a red ball
# (no motor control is performed to move the camera, we will get to that later in the tutorial)

import cv2
import numpy as np
import os


def nothing(x):
    pass


###################################################################################################
def main():




    cv2.namedWindow('image')
    cv2.createTrackbar('LowH', 'image', 1, 255, nothing)
    cv2.createTrackbar('HighH', 'image', 1, 255, nothing)
    cv2.createTrackbar('LowS', 'image', 1, 255, nothing)
    cv2.createTrackbar('HighS', 'image', 1, 255, nothing)
    cv2.createTrackbar('LowV', 'image', 1, 255, nothing)
    cv2.createTrackbar('HighV', 'image', 1, 255, nothing)
    cv2.createTrackbar('dp', 'image', 1, 255, nothing)
    cv2.createTrackbar('minDist', 'image', 1, 255, nothing)
    cv2.createTrackbar('param1', 'image', 1, 255, nothing)
    cv2.createTrackbar('param2', 'image', 1, 255, nothing)
    cv2.namedWindow("imgOriginal", cv2.WINDOW_AUTOSIZE)  # create windows, use WINDOW_AUTOSIZE for a fixed window size
    cv2.namedWindow("imgMorph", cv2.WINDOW_AUTOSIZE)
    cv2.namedWindow("imgMorph", cv2.WINDOW_AUTOSIZE)
    imgOriginal = cv2.imread('2016-04-19-204133.jpg',
                                 1)    
    imgOriginal = cv2.resize(imgOriginal, (320,240))

    while(cv2.waitKey(1) != 27):

        imgHSV = cv2.cvtColor(imgOriginal, cv2.COLOR_BGR2HSV)

        LowH = cv2.getTrackbarPos('LowH', 'image')
        HighH = cv2.getTrackbarPos('HighH', 'image')

        LowS = cv2.getTrackbarPos('LowS', 'image')
        HighS = cv2.getTrackbarPos('HighS', 'image')

        LowV = cv2.getTrackbarPos('LowV', 'image')
        HighV = cv2.getTrackbarPos('HighV', 'image')

        minD = cv2.getTrackbarPos('minDist', 'image')
        param1 = cv2.getTrackbarPos('param1', 'image')
        param2 = cv2.getTrackbarPos('param2', 'image')
        dp = cv2.getTrackbarPos('dp', 'image')

        #        imgThresh = cv2.inRange(imgHSV, np.array([153, 29, 106]), np.array([184, 70, 255])) #Pink Ball

        #        imgThresh = cv2.inRange(imgHSV, np.array([168, 119, 63]), np.array([180, 255, 197])) #Red Ball Daylight
        #        imgThresh = cv2.inRange(imgHSV, np.array([154, 255, 37]), np.array([190, 255, 255])) #Red ball night

        #        imgThresh = cv2.inRange(imgHSV, np.array([78, 128, 0]), np.array([141, 255, 255]))
        imgThresh = cv2.inRange(imgHSV, np.array([LowH, LowS, LowV]), np.array([HighH, HighS, HighV]))


        imgDial = cv2.dilate(imgThresh, np.ones((5, 5), np.uint8))
        imgErode = cv2.erode(imgDial, np.ones((5, 5), np.uint8))

        str_el = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
        morph = cv2.morphologyEx(imgThresh, cv2.MORPH_OPEN, str_el)
        morph = cv2.morphologyEx(morph, cv2.MORPH_CLOSE, str_el)
        
        imgCircle = circleDetected(morph, imgOriginal, minD)

        cv2.imshow("imgOriginal", imgCircle)  # show windows
        cv2.imshow("imgErode", imgErode)
        cv2.imshow("imgMorph", morph)

    # end while

    #cv2.waitKey(0)
    #cv2.destroyAllWindows()                     # remove windows from memory

    return
###################################################################################################

def circleDetected(image, imgOriginal, minD):
    cont, contours, hierarchy = cv2.findContours(image, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    cicleImg = cv2.copyMakeBorder(imgOriginal,0,0,0,0,cv2.BORDER_REPLICATE)
    for i in range(len(contours)):
        (x, y), r = cv2.minEnclosingCircle(contours[i])
        if (r >= minD):
            cv2.circle(cicleImg, (int(x), int(y)), int(r), (0, 0, 255), 3)
            #intRows, intColumns = imgErode.shape
    return cicleImg

###################################################################################################
if __name__ == "__main__":
    main()
