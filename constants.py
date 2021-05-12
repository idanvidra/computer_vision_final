import cv2 

ROBOT_IP = '192.168.57.30'

MOTOR_NAME = "bottom"

BUFF = 1024

HOST = '192.168.56.167'

PORT = 12345

ADDRESS = (HOST, PORT)

FULL_CIRCLE = 4096

THIRD_CIRCLE = int(FULL_CIRCLE / 3)

STEP = 100

lk_params = dict( winSize  = (13, 13),
                  maxLevel = 1,
                  criteria = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 15, 0.08))

lk_params_advanced = dict( winSize  = (15, 15),
                           maxLevel = 2,
                           criteria = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03))

feature_params = dict( maxCorners = 10,
                       qualityLevel = 0.3,
                       minDistance = 7,
                       blockSize = 7 )

# the upper and lower ranges of the
# HSV required for particular colour
upper_hue = 153
upper_saturation = 255
upper_value = 255
lower_hue = 64
lower_saturation = 72
lower_value = 49