import cv2 

ROBOT_IP = '192.168.56.188'

MOTOR_NAME = "buttom"

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