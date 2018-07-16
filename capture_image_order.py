import cv2
import numpy as np

# Create a video capture object
camera = cv2.VideoCapture(1)

camera.set(3, 1280) # set the resolution
camera.set(4, 720)

def image_capture(video = True):
    #Set frame rate
    #camera.set(cv2.cv.CV_CAP_PROP_FPS, frame_rate)

    grabbed, frame = camera.read()
    abc = frame
    return frame
if __name__ == '__main__':

    while True:
        # Get the input image
        image = image_capture()
        cv2.imshow('Frame',image)
        # Break if cv2 window is open by pressig "q" button.
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
