import cv2
import numpy as np

# Create a video capture object
camera = cv2.VideoCapture(1)


camera.set(3, 1280) # set the resolution
camera.set(4, 720)
camera.set(cv2.CAP_PROP_AUTOFOCUS, 0) # turn the autofocus off

def image_capture(frame_rate = 10 , image_resolution = (640, 480) ,  verbose = False):
    #Set frame rate
    #camera.set(cv2.cv.CV_CAP_PROP_FPS, frame_rate)

    (grabbed, frame) = camera.read()
    return frame

if __name__ == '__main__':


    while True:
        # Get the input image
        image = image_capture()
        cv2.imshow('Frame',image)
        # Break if cv2 window is open by pressig "q" button.
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
