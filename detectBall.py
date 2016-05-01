import cv2
import numpy as np
import sys
import os
import io
import datetime
import Calibration

IS_PI = False

if (IS_PI):
    import picamera

CAM_LOCATION = 0

def main():

    calib = []
    for i in range(1,2):

        filename = takePicture()
        calibRes = Calibration.calibration(filename) #calibrate camera many times to average the calibration
        calib.append(calibRes)

    capWebcam = openCamera()

    while capWebcam.isOpened():
        blnFrameReadSuccessfully, imgOriginal = capWebcam.read()  # read next frame

        if not blnFrameReadSuccessfully or imgOriginal is None:  # if frame was not read successfully
            print "error: frame not read from webcam\n"  # print error message to std out
            os.system("pause")  # pause until user presses a key so user can see error message
            break

            #get location of ball
        filteredImg = Calibration.filterImage(imgOriginal,(calib[0])[0], (calib[0])[1])

        print location(filteredImg)

    #endWhile


def location(filteredImg):
    maxRadius, xMax, yMax = (0, 0,0)
    cont, contours, hierarchy = cv2.findContours(filteredImg, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

    for i in range(len(contours)):
        (x, y), r = cv2.minEnclosingCircle(contours[i])
        if (maxRadius < r):
            maxRadius = r
            xMax = x
            yMax = y

    return (xMax, yMax, maxRadius)

###################################################################################################

def openCamera():

    if (IS_PI):
        stream = io.BytesIO()
        with picamera.PiCamera() as camera:
            camera.framerate = 10
            camera.start_preview()
            camera.capture(stream, format='jpeg')

            data = np.fromstring(stream.getvalue(), dtype=np.uint8)
            cam = image = cv2.imdecode(data, 1)
    else:
        cam = capWebcam = cv2.VideoCapture(CAM_LOCATION)

    if capWebcam.isOpened() == False:                           # check if VideoCapture object was associated to webcam successfully
        print "error: capWebcam not accessed successfully\n\n"          # if not, print error message to std out
        sys.exit(-1)                                       # pause until user presses a key so user can see error message

    return cam
###################################################################################################
def takePicture():
    filename = 'Pics/' + str(datetime.datetime.now()) + '.png'

    cam = openCamera()
    s, im = cam.read()
    cv2.imwrite(filename, im)
    cam.release()
    return filename
###################################################################################################

if __name__ == "__main__":
    #main(sys.argv)
    main()