import cv2
import Calibration
from imutils.video import VideoStream
import datetime
import time

IS_PI = False

CAM_LOCATION = 0

def main():
    calib = []
    for i in range(1, 2):
        filename = takePicture()
        calibRes = Calibration.calibration(filename)  # calibrate camera many times to average the calibration
        calib.append(calibRes)

    capWebcam = openCamera()

    while True:
        imgOriginal = capWebcam.read()  # read next frame

        # get location of ball
        filteredImg = Calibration.filterImage(imgOriginal, (calib[0])[0], (calib[0])[1])

        print location(filteredImg)

        # endWhile


def location(filteredImg):
    maxRadius, xMax, yMax = (0, 0, 0)
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
        vs = VideoStream(usePiCamera=1).start()

    else:
        vs = VideoStream()

    time.sleep(2.0)

    return vs


###################################################################################################
def takePicture():
    filename = 'Pics/' + str(datetime.datetime.now()) + '.png'

    cam = openCamera()
    im = cam.read()
    cv2.imwrite(filename, im)
    cam.stop()
    return filename


###################################################################################################

if __name__ == "__main__":
    # main(sys.argv)
    main()
