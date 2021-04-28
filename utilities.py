import cv2 
import numpy as np
from constants import *
from arm_movement_control import ArmMotorControl

# creates arm object and sets moving speed and acceleration
def init_arm(speed = 120, acceleration = 2):
    arm = ArmMotorControl()
    arm.set_moving_speed(MOTOR_NAME, speed)
    arm.set_acceleration(MOTOR_NAME, acceleration)
    
    return arm

# recieves x,y coordinates and reshapes them into array
def coordinate_shaper(x,y):
    return np.array([[x, y]], dtype=np.float32).reshape(-1,1,2)

# compares x coordinates to check for movement and direction (x axis only) on camera
# if movement was detected the arm is moved accordingly
def check_movement(x, ox, sensativity=10, arm=None):
    if x > ox + sensativity: 
        print("moved right")
        # arm.turn_clockwise(MOTOR_NAME)
    if x < ox - sensativity: 
        print("moved left ")
        # arm.turn_counter_clockwise(MOTOR_NAME)

