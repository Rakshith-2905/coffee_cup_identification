import cv2
import cv2.aruco as aruco
import numpy as np

def read_tag(frame,display = False):
    ids = None
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    aruco_dict = aruco.Dictionary_get(aruco.DICT_4X4_50)
    parameters =  aruco.DetectorParameters_create()

    # #lists of ids and the corners beloning to each id
    corners, ids, rejectedImgPoints = aruco.detectMarkers(gray, aruco_dict, parameters=parameters)
    #gray = aruco.drawDetectedMarkers(frame, corners)

    #print(rejectedImgPoints)
    # Display the resulting frame
    #cv2.imshow('order_frame',gray)
    if(len(corners)>0):
        return ids
