import cv2
import cv2.aruco as aruco
from capture_image_table import image_capture
from read_db import get_data
import numpy as np


previous_corner = 0
cv2.namedWindow("projection_view", cv2.WND_PROP_FULLSCREEN)
cv2.setWindowProperty("projection_view",cv2.WND_PROP_FULLSCREEN,cv2.WINDOW_FULLSCREEN)

def caliberateAruco(frame):

    # Create a black image
    img_dst = np.zeros((2160,3840,3), np.uint8)
    img_src = frame # 720 X 1280
    img_src1 = np.zeros((720,1280,3), np.uint8)

    pts_dst = np.array([[1850,750],[1950,750],[1950,850],[1850,850]])#[[1850,750],[1950,750],[1950,850],[1850,850]])#Lefttop,LeftBottom,RightBottom,RightTop#np.array([[0,0],[0,100],[100,100],[100,0]])#Lefttop,LeftBottom,RightBottom,RightTop
    # pts_dst = pts_dst.reshape((-1,1,2))
    # cv2.polylines(blank_image_dst,[pts_dst],True,(0,255,255))
    print("calib")
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    aruco_dict = aruco.Dictionary_get(aruco.DICT_6X6_250)
    parameters =  aruco.DetectorParameters_create()

    # pts_dst = np.array([[1450,1450],[1450,1550],[1550,1550],[1550,1450]])

        #lists of ids and the corners beloning to each id
    corners, ids, rejectedImgPoints = aruco.detectMarkers(gray, aruco_dict, parameters=parameters)

    if len(corners) > 0:
        for counter, value in enumerate(ids):
                #print(corners[counter],counter)
                # converting corners to pixel
                x1 = (int(corners[counter][0][0][0]), int(corners[counter][0][0][1]))
                x2 = (int(corners[counter][0][1][0]), int(corners[counter][0][1][1]))
                x3 = (int(corners[counter][0][2][0]), int(corners[counter][0][2][1]))
                x4 = (int(corners[counter][0][3][0]), int(corners[counter][0][3][1]))

                circle_center = (int(((x1[0]+x2[0]+x3[0]+x4[0])/4)),int(((x1[1]+x2[1]+x3[1]+x4[1])/4)+50))
                cv2.circle(img_src1, circle_center, 280, (255, 255, 255), -1)

                pts_src = np.array([[x1[0],x1[1]],[x2[0],x2[1]],[x3[0],x3[1]],[x4[0],x4[1]]])
                print(pts_src)
                try:
                    h = np.load('homography.npy')
                    print(h)
                except:
                    h, status = cv2.findHomography(pts_src, pts_dst)
                    np.save('homography.npy', h)
                    print(h)

                img_wraped = cv2.warpPerspective(img_src1, h, (img_dst.shape[1], img_dst.shape[0]))
                cv2.imshow('image_projected',img_wraped)
                cv2.waitKey(0)
                return h



def read_tag(frame,h,display = False):
    global previous_corner

    colors = {0:(255, 255, 255),\
              1:(230, 25, 75),\
              2:(60, 180, 75),\
              3:(255, 225, 25),\
              4:(0, 130, 200),\
              5:(245, 130, 48),\
              6:(145, 30, 180),\
              7:(170, 110, 40),\
              8:(255, 250, 200),\
              9:(240, 50, 230)}

    # Camera internals
    size = frame.shape


    # Create a blank image for displaying the circles
    blank_image_src = np.zeros(size, np.uint8)
    blank_image_dst = np.zeros((2160,3840,3), np.uint8)
    display = np.zeros((1080,1000,3), np.uint8)

    #img_wraped = np.zeros((2160,3840,3), np.uint8)

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # thresh = 127
    # gray = cv2.threshold(gray, thresh, 255, cv2.THRESH_BINARY)[1]
    aruco_dict = aruco.Dictionary_get(aruco.DICT_4X4_50)
    parameters =  aruco.DetectorParameters_create()

    #print(parameters)

    '''    detectMarkers(...)
        detectMarkers(image, dictionary[, corners[, ids[, parameters[, rejectedI
        mgPoints]]]]) -> corners, ids, rejectedImgPoints
        '''
        #lists of ids and the corners beloning to each id
    corners, ids, rejectedImgPoints = aruco.detectMarkers(gray, aruco_dict, parameters=parameters)

    border = np.array([[10,10],[1270,10],[1270,710],[10,710]])#Lefttop,RightTop,RightBottom,LeftBottom
    border = border.reshape((-1,1,2))
    cv2.polylines(blank_image_src,[border],True,(0,255,0))

    if (abs(len(corners)-previous_corner)) > 0:

        if(len(corners)>0):
            for counter, value in enumerate(ids):

                    data = get_data(value)
                    if data:

                        id,name,drink = data[0][0],data[0][1],data[0][2]

                        # converting corners to pixel
                        x1 = (int(corners[counter][0][0][0]), int(corners[counter][0][0][1]))
                        x2 = (int(corners[counter][0][1][0]), int(corners[counter][0][1][1]))
                        x3 = (int(corners[counter][0][2][0]), int(corners[counter][0][2][1]))
                        x4 = (int(corners[counter][0][3][0]), int(corners[counter][0][3][1]))

                        circle_center = (int(((x1[0]+x2[0]+x3[0]+x4[0])/4)+50),int(((x1[1]+x2[1]+x3[1]+x4[1])/4)+50))
                        cv2.circle(blank_image_src, circle_center, 120, colors[id], -1)

                        # #font type hershey_simpex
                        font = cv2.FONT_HERSHEY_SIMPLEX
                        cv2.putText(blank_image_src, str(name + '\'s'+ ' ' + drink), (int(circle_center[0]-80),int(circle_center[1]+150)), font, 1, colors[id+1], 2, cv2.LINE_AA)

                        img_wraped = cv2.warpPerspective(blank_image_src, h, (blank_image_dst.shape[1], blank_image_dst.shape[0]))

                        if counter == 0:
                            cv2.putText(display, str(name + '\'s'+ ' ' + drink), (10,50), font, 1, colors[id+1], 2, cv2.LINE_AA)
                            cv2.circle(display, (500,50), 20, colors[id], -1)

                        else:
                            cv2.putText(display, str(name + '\'s'+ ' ' + drink), (10,(100*(counter))), font, 1, colors[id+1], 2, cv2.LINE_AA)
                            cv2.circle(display, (500,(100*(counter))), 20, colors[id], -1)
                        previous_corner = len(corners)
        else:
            previous_corner = 0
            # Create a blank image for displaying the circles
            blank_image_src = np.zeros(size, np.uint8)

            border = np.array([[10,10],[1270,10],[1270,710],[10,710]])#Lefttop,RightTop,RightBottom,LeftBottom
            border = border.reshape((-1,1,2))
            cv2.polylines(blank_image_src,[border],True,(0,255,0))
            img_wraped = cv2.warpPerspective(blank_image_src, h, (blank_image_dst.shape[1], blank_image_dst.shape[0]))
        cv2.imshow('projection_view',img_wraped)
        cv2.imshow('display',display)

    gray = aruco.drawDetectedMarkers(frame, corners)

    # if display:
    # Display the resulting frame
    #cv2.imshow('camera_view',gray)

    return ids,corners


if __name__ == '__main__':

    h = None
    try:
        h = np.load('homography.npy')
    except:
    #Create a black image
        img_dst = np.zeros((2160,3840,3), np.uint8)
        pts_dst = np.array([[1850,750],[1950,750],[1950,850],[1850,850]])#Lefttop,RightTop,RightBottom,LeftBottom
        pts = pts_dst.reshape((-1,1,2))
        cv2.polylines(img_dst,[pts],True,(0,255,255))
        cv2.circle(img_dst, (1900,800), 200, (255,255,255), 1)
        # #font type hershey_simpex
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(img_dst, "Place the caliberation cup on the square", (1080,1920), font, 1, (255,255,255), 4, cv2.LINE_AA)

        cv2.imshow('image_realword',img_dst)
        cv2.waitKey(0)
        while not h:
            image = image_capture()
            h = caliberateAruco(image)

    while True:
        # Get the input image
        image = image_capture()
        data = read_tag(image,h,True)

        # Break if cv2 window is open by pressig "q" button.
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
