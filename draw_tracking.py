import numpy as np
import cv2
from utilities import *


class draw_tracker:

    def __init__(self):
        # robot arm control
        # self.arm = init_arm()
        a=5

    # default called trackbar function 
    def setValues(self, x):
        print("")

    def start(self):
        # Creating the trackbars needed for 
        # adjusting the marker colour These 
        # trackbars will be used for setting 
        # the upper and lower ranges of the
        # HSV required for particular colour
        cv2.namedWindow("Color detectors")
        cv2.createTrackbar("Upper Hue", "Color detectors",
                        153, 180, self.setValues)
        cv2.createTrackbar("Upper Saturation", "Color detectors",
                        255, 255, self.setValues)
        cv2.createTrackbar("Upper Value", "Color detectors", 
                        255, 255, self.setValues)
        cv2.createTrackbar("Lower Hue", "Color detectors",
                        64, 180, self.setValues)
        cv2.createTrackbar("Lower Saturation", "Color detectors", 
                        72, 255, self.setValues)
        cv2.createTrackbar("Lower Value", "Color detectors", 
                        49, 255, self.setValues)
        
        # The kernel to be used for dilation purpose 
        kernel = np.ones((5, 5), np.uint8)
        
        # Loading the default webcam of PC.
        cap = cv2.VideoCapture(0)

        # init random starting coordinates
        ox, oy = 250,250
        previous_coordinates = coordinate_shaper(ox,oy)

        # Keep looping
        while True:
            
            # Reading the frame from the camera
            ret, frame = cap.read()
            
            # Flipping the frame to see same side of yours
            frame = cv2.flip(frame, 1)
            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        
            # Getting the updated positions of the trackbar
            # and setting the HSV values
            u_hue = cv2.getTrackbarPos("Upper Hue",
                                    "Color detectors")
            u_saturation = cv2.getTrackbarPos("Upper Saturation",
                                            "Color detectors")
            u_value = cv2.getTrackbarPos("Upper Value",
                                        "Color detectors")
            l_hue = cv2.getTrackbarPos("Lower Hue",
                                    "Color detectors")
            l_saturation = cv2.getTrackbarPos("Lower Saturation",
                                            "Color detectors")
            l_value = cv2.getTrackbarPos("Lower Value",
                                        "Color detectors")
            Upper_hsv = np.array([u_hue, u_saturation, u_value])
            Lower_hsv = np.array([l_hue, l_saturation, l_value])   
        
            # Identifying the pointer by making its 
            # mask
            Mask = cv2.inRange(hsv, Lower_hsv, Upper_hsv)
            Mask = cv2.erode(Mask, kernel, iterations = 1)
            Mask = cv2.morphologyEx(Mask, cv2.MORPH_OPEN, kernel)
            Mask = cv2.dilate(Mask, kernel, iterations = 1)
        
            # Find contours for the pointer after 
            # idetifying it
            cnts, _ = cv2.findContours(Mask.copy(), cv2.RETR_EXTERNAL,
                cv2.CHAIN_APPROX_SIMPLE)
            center = None

            # If the contours are formed
            if len(cnts) > 0:
                
                # sorting the contours to find biggest 
                cnt = sorted(cnts, key = cv2.contourArea, reverse = True)[0]
                
                # Get the radius of the enclosing circle 
                # around the found contour
                ((x, y), radius) = cv2.minEnclosingCircle(cnt)
                
                # Draw the circle around the contour
                cv2.circle(frame, (int(x), int(y)), int(radius), (0, 255, 255), 2)
                cv2.circle(frame, (int(x), int(y)), 6, (0,255,0), -1)
                
                # Calculating the center of the detected contour
                M = cv2.moments(cnt)
                center = (int(M['m10'] / M['m00']), int(M['m01'] / M['m00']))
                

            current_coordinates = coordinate_shaper(x,y)
            for i, j in zip(previous_coordinates, current_coordinates):
                x,y = j.ravel()
                ox,oy = i.ravel()

                cv2.line(frame, (ox,oy), (x,y), (0,0,255), 2)

                # moving condition
                check_movement(x=x, ox=ox, sensativity=10)

            previous_coordinates = current_coordinates.reshape(-1,1,2)
                

            # Show all the windows
            cv2.imshow("Tracking", frame)
            cv2.imshow("mask", Mask)
        
            # If the 'q' key is pressed then stop the application 
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break
        
        # Release the camera and all resources
        cap.release()
        cv2.destroyAllWindows()