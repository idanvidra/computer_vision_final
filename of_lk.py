import cv2 
import numpy as np
from constants import *
from utilities import *
from arm_movement_control import ArmMotorControl

# init
x = 150
y = 150
stage = -1 # what is k?
video_capture = cv2.VideoCapture(0)

# robot arm control
# arm = init_arm()

# mouse click handler for initial tracking coordinate selection
def mouse_click_input_handler(event, clicked_x, clicked_y, flag, parameter):
    if event == cv2.EVENT_LBUTTONDOWN:
        global x,y,stage
        x = clicked_x
        y = clicked_y
        stage = 1

cv2.namedWindow("Tracking Coordinate Selection")
cv2.setMouseCallback("Tracking Coordinate Selection", mouse_click_input_handler)

# inital tracking coordinate selection
while True:
     
    read_correctly, video_image = video_capture.read()
    video_image = cv2.flip(video_image, 1)
    gray_video_image = cv2.cvtColor(video_image, cv2.COLOR_BGR2GRAY)
    
    cv2.imshow("Tracking Coordinate Selection", video_image)
    
    if stage == 1 or cv2.waitKey(30) == 27:
        cv2.destroyAllWindows()
        break


# init coordinate vector and mask
previous_coordinates = coordinate_shaper(x,y)
mask = np.zeros_like(video_image)

# main OF tracking loop
while True:

    read_correctly, current_video_image = video_capture.read()
    current_video_image = cv2.flip(current_video_image, 1)
    current_gray_video_image = cv2.cvtColor(current_video_image, cv2.COLOR_BGR2GRAY)

    # Optical flow
    current_coordinates,f,e = cv2.calcOpticalFlowPyrLK(gray_video_image,
                                                       current_gray_video_image,
                                                       previous_coordinates,
                                                       None,
                                                       maxLevel=1,
                                                       criteria=OF_CRITERIA)

    for i, j in zip(previous_coordinates, current_coordinates):
        x,y = j.ravel()
        ox,oy = i.ravel()

        # draw line and dot current coordinates
        mask = cv2.line(mask, (ox,oy), (x,y), (0,0,255), 5)
        cv2.circle(current_video_image, (x,y), 6, (0,255,0), -1)

        # moving condition
        check_movement(x=x, ox=ox, sensativity=10)
        

    # show changes on image
    current_video_image = cv2.addWeighted(mask, 0.3, current_video_image, 0.7, 0)

    # show to screen
    cv2.imshow("ouput", current_video_image)
    cv2.imshow("result", mask)

    # reset image and coordinates to current
    gray_video_image = current_gray_video_image.copy()
    previous_coordinates = current_coordinates.reshape(-1,1,2)
    
    if cv2.waitKey(1) & 0xff == 27:
        break

cv2.destroyAllWindows()
video_capture.release()