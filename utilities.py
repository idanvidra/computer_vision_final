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


# check distance given and move KIP accordingly
def check_movement(d, sensativity=10, arm=None):

    # we multiply by 30 to make up for the difference between dynamixell and pixel 
    # diffreneces - where dynamixell is the measurement for the robots motors
    movement = int(30*abs(np.ceil(d)))
    if d > sensativity: 
        print("moved right")
        arm.turn_clockwise(MOTOR_NAME,movement)
    if d < - sensativity: 
        print("moved left ")
        
        arm.turn_counter_clockwise(MOTOR_NAME, movement)
