# opencv_playground
Ball Detection in opencv.

This code is a framework I am building to detect a ball and its location to pass to a rover.

The code calibrates based on the object in the front of the camera when it starts up. It takes photos and then processes them.
To do this we take the image and go though many different HSV values to see if we can detect large objects. Once this is done we sort the results based on the size(max) of the object detected and the minimum amount of noise on the image.

This routine expects that the ball or object is in-front of the camera for detection. 
Once this detection routine is completed we start the video and tracking.

This gives us the location of the ball in the video frames.

