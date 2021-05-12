import numpy as np
import cv2

from utilities import *
from constants import *

class draw_tracker:

    def __init__(self):
        # robot arm control
        self.arm = init_arm()

    def start(self):
        
        # The kernel to be used for dilation purpose 
        kernel = np.ones((5, 5), np.uint8)
        
        # Loading the default webcam of PC.
        cap = cv2.VideoCapture(0)

        # init starting coordinates
        ox, oy = 250,250
        x,y=0,0
        previous_coordinates = coordinate_shaper(ox,oy)

        

        # main loop
        while True:
            
            # reading the frame from the camera
            ret, frame = cap.read()
            
            # flipping the frame to see same side of yours
            frame = cv2.flip(frame, 1)
            # hsv copy of the frame
            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

            # set the HSV ranges - collected from constants
            upper_hsv = np.array([upper_hue, upper_saturation, upper_value])
            lower_hsv = np.array([lower_hue, lower_saturation, lower_value])
        
            # make the image binary by the HSV ranges
            mask = cv2.inRange(hsv, lower_hsv, upper_hsv)

            # use morphological functions to open and close the binary image
            mask = cv2.erode(mask, kernel, iterations = 1)
            mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
            mask = cv2.dilate(mask, kernel, iterations = 1)
        
            # find contours for the pointer after idetifying it
            cnts, _ = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
                cv2.CHAIN_APPROX_SIMPLE)
            center = None

            
            # if the contours are formed
            if len(cnts) > 0:
                
                # sorting the contours to find biggest 
                cnt = sorted(cnts, key = cv2.contourArea, reverse = True)[0]
                
                # get the radius of the enclosing circle around the found contour
                ((x, y), radius) = cv2.minEnclosingCircle(cnt)
                
                # draw the circle around the contour
                cv2.circle(frame, (int(x), int(y)), int(radius), (0, 255, 255), 2)

                # mark center with red circle
                cv2.circle(frame, (int(x), int(y)), 6, (0,255,0), -1)
                
                # calculating the center of the detected contour using moments:
                # some pixels on the contour get "weights" according to their
                # brightness and the "center of mass" is located accordingly
                M = cv2.moments(cnt)
                center = (int(M['m10'] / M['m00']), int(M['m01'] / M['m00']))

            current_coordinates = coordinate_shaper(x,y)
            for i, j in zip(previous_coordinates, current_coordinates):
                x,y = j.ravel()
                ox,oy = i.ravel()

                cv2.line(frame, (ox,oy), (x,y), (0,0,255), 2)

                # calculate difference to test for movement
                d = x - ox

                # moving condition
                check_movement(d=d, sensativity=2, arm=self.arm)

            previous_coordinates = current_coordinates.reshape(-1,1,2)
                

            # Show all the windows
            cv2.imshow("Tracking", frame)
            cv2.imshow("mask", mask)
        
            # If the 'q' key is pressed then stop the application 
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break
        
        # Release the camera and all resources
        cap.release()
        cv2.destroyAllWindows()

def main():
    draw_tracker().start()
    print('Done')


if __name__ == '__main__':
    main()
    cv2.destroyAllWindows()