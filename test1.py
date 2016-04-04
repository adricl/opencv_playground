#OpenCV_test_3.py

# this program tracks a red ball
# (no motor control is performed to move the camera, we will get to that later in the tutorial)

import cv2
import numpy as np
import os

def nothing(x):
    pass

###################################################################################################
def main():

    capWebcam = cv2.VideoCapture(0)                     # declare a VideoCapture object and associate to webcam, 0 => use 1st webcam

                                                        # show original resolution
    print "default resolution = " + str(capWebcam.get(cv2.CAP_PROP_FRAME_WIDTH)) + "x" + str(capWebcam.get(cv2.CAP_PROP_FRAME_HEIGHT))

#    capWebcam.set(cv2.CAP_PROP_FRAME_WIDTH, 320.0)              # change resolution to 320x240 for faster processing
#    capWebcam.set(cv2.CAP_PROP_FRAME_HEIGHT, 240.0)

                                                        # show updated resolution
    print "updated resolution = " + str(capWebcam.get(cv2.CAP_PROP_FRAME_WIDTH)) + "x" + str(capWebcam.get(cv2.CAP_PROP_FRAME_HEIGHT))

    if capWebcam.isOpened() == False:                           # check if VideoCapture object was associated to webcam successfully
        print "error: capWebcam not accessed successfully\n\n"          # if not, print error message to std out
        os.system("pause")                                              # pause until user presses a key so user can see error message
        return                                                          # and exit function (which exits program)
    # end if

    


    cv2.namedWindow('image')
    cv2.createTrackbar('LowH','image',0,255,nothing)
    cv2.createTrackbar('HighH','image',0,255,nothing)
    cv2.createTrackbar('LowS','image',0,255,nothing)
    cv2.createTrackbar('HighS','image',0,255,nothing)
    cv2.createTrackbar('LowV','image',0,255,nothing)
    cv2.createTrackbar('HighV','image',0,255,nothing)
    cv2.createTrackbar('dp','image',1,255,nothing)
    cv2.createTrackbar('minDist','image',1,255,nothing)
    cv2.createTrackbar('param1','image',1,255,nothing)
    cv2.createTrackbar('param2','image',1,255,nothing)


    while cv2.waitKey(1) != 27 and capWebcam.isOpened():                # until the Esc key is pressed or webcam connection is lost
        blnFrameReadSuccessfully, imgOriginal = capWebcam.read()            # read next frame

        if not blnFrameReadSuccessfully or imgOriginal is None:             # if frame was not read successfully
            print "error: frame not read from webcam\n"                     # print error message to std out
            os.system("pause")                                              # pause until user presses a key so user can see error message
            break                                                           # exit while loop (which exits program)
        # end if

        imgHSV = cv2.cvtColor(imgOriginal, cv2.COLOR_BGR2HSV)

        LowH = cv2.getTrackbarPos('LowH','image')
        HighH = cv2.getTrackbarPos('HighH','image')

        LowS = cv2.getTrackbarPos('LowS','image')
        HighS = cv2.getTrackbarPos('HighS','image')

        LowV = cv2.getTrackbarPos('LowV','image')
        HighV = cv2.getTrackbarPos('HighV','image')

#        imgThresh = cv2.inRange(imgHSV, np.array([153, 29, 106]), np.array([184, 70, 255])) #Pink Ball

#        imgThresh = cv2.inRange(imgHSV, np.array([168, 119, 63]), np.array([180, 255, 197])) #Red Ball Daylight
        imgThresh = cv2.inRange(imgHSV, np.array([154, 255, 37]), np.array([190, 255, 255])) #Red ball night
#        imgThresh = cv2.inRange(imgHSV, np.array([LowH, LowS, LowV]), np.array([HighH, HighS, HighV]))
#        imgThresh = cv2.add(imgThreshLow, imgThreshHigh)


#        imgErode = cv.cvSmooth(imgThresh, CV_GAUSSIAN, 9, 9)
        imgGau = cv2.GaussianBlur(imgThresh, (3, 3), 2)
#	imgThresh = cv2.Th
        imgDial = cv2.dilate(imgGau, np.ones((5,5),np.uint8))
        imgErode = cv2.erode(imgDial, np.ones((5,5),np.uint8))

        intRows, intColumns = imgErode.shape


#        circles = cv2.HoughCircles(imgErode, cv2.HOUGH_GRADIENT, 5, intRows / 5)      # fill variable circles with all circles in the processed image
        minD = cv2.getTrackbarPos('minDist','image')
        param1 = cv2.getTrackbarPos('param1','image')
        param2 = cv2.getTrackbarPos('param2','image')
        dp = cv2.getTrackbarPos('dp','image')
        
        circles = cv2.HoughCircles(imgThresh, cv2.HOUGH_GRADIENT, dp, intRows/2)
        if circles is not None:                     # this line is necessary to keep program from crashing on next line if no circles were found
            print "balls " + str(circles.size)
            for circle in circles[0]:                           # for each circle
                x, y, radius = circle                                                                       # break out x, y, and radius
                print "x " + str(x) + " y " + str(y) + " intCol " + str(intColumns) + " intRows " + str(intRows)
                if ((x > 0) & (x < intRows) & (y > 0) & (y < intColumns)):
                    print "ball position x = " + str(x) + ", y = " + str(y) + ", radius = " + str(radius)       # print ball position and radius
                    cv2.circle(imgOriginal, (x, y), 3, (0, 255, 0), -1)           # draw small green circle at center of detected object
                    cv2.circle(imgOriginal, (x, y), radius, (0, 0, 255), 3)                     # draw red circle around the detected object
            # end for
        # end if

        cv2.namedWindow("imgOriginal", cv2.WINDOW_AUTOSIZE)            # create windows, use WINDOW_AUTOSIZE for a fixed window size
#        cv2.namedWindow("imgThresh", cv2.WINDOW_AUTOSIZE)           # or use WINDOW_NORMAL to allow window resizing
#        cv2.namedWindow("imgGaus", cv2.WINDOW_AUTOSIZE)
#        cv2.namedWindow("imgDial", cv2.WINDOW_AUTOSIZE)
#        cv2.namedWindow("imgErode", cv2.WINDOW_AUTOSIZE)
#        cv2.namedWindow("imgHSV", cv2.WINDOW_AUTOSIZE)
#        cv2.namedWindow("imgErode", cv2.WINDOW_AUTOSIZE)
#        cv2.namedWindow("imgHSV", cv2.WINDOW_AUTOSIZE)

#        cv2.namedWindow("imgThreshLow", cv2.WINDOW_AUTOSIZE)
#        cv2.namedWindow("imgThreshHigh", cv2.WINDOW_AUTOSIZE)

#        cv2.imshow("imgThreshLow", imgThreshLow)                 # show windows
#        cv2.imshow("imgThreshHigh", imgThreshHigh)

        cv2.imshow("imgOriginal", imgOriginal)                 # show windows
        #cv2.imshow("imgThresh", imgThresh)
        #cv2.imshow("imgHSV", imgHSV)
        #cv2.imshow("imgGaus", imgGau)
        #cv2.imshow("imgDial", imgDial)
        cv2.imshow("imgErode", imgErode)

    # end while

    cv2.destroyAllWindows()                     # remove windows from memory

    return

###################################################################################################
if __name__ == "__main__":
    main()

