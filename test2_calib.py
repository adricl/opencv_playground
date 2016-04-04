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

    while cv2.waitKey(1) != 27 and capWebcam.isOpened():                # until the Esc key is pressed or webcam connection is lost
        blnFrameReadSuccessfully, imgOriginal = capWebcam.read()            # read next frame

        if not blnFrameReadSuccessfully or imgOriginal is None:             # if frame was not read successfully
            print "error: frame not read from webcam\n"                     # print error message to std out
            os.system("pause")                                              # pause until user presses a key so user can see error message
            break                                                           # exit while loop (which exits program)
        # end if

        #Base State
        vals = [0,0,0,255,255,255]
        maxVar = 0
        bestVal = [0,0,0,255,255,255]
        state = 0
        
        for num in range(0,255)

        circles_detected(vals, imgOriginal)

        cv2.namedWindow("imgOriginal", cv2.WINDOW_AUTOSIZE)            # create windows, use WINDOW_AUTOSIZE for a fixed window size
        cv2.imshow("imgOriginal", imgOriginal)                 # show windows




    # end while

    cv2.destroyAllWindows()                     # remove windows from memory

    return
###################################################################################################

def circles_detected (vals, imgOriginal):
        imgHSV = cv2.cvtColor(imgOriginal, cv2.COLOR_BGR2HSV)
        imgThresh = cv2.inRange(imgHSV, np.array([vals[0], vals[1], vals[2]]), np.array([vals[3], vals[4], vals[5]]))
        imgGau = cv2.GaussianBlur(imgThresh, (3, 3), 2)
        imgDial = cv2.dilate(imgGau, np.ones((5,5),np.uint8))
        imgErode = cv2.erode(imgDial, np.ones((5,5),np.uint8))
        cv2.imshow("imgErode", imgErode)
        intRows, intColumns = imgErode.shape

        circles = cv2.HoughCircles(imgThresh, cv2.HOUGH_GRADIENT, 4, 1)
        if circles is not None:
            return circles.size 
        return 0

###################################################################################################
if __name__ == "__main__":
    main()


