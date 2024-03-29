from butter_connector import ButterConnector
from constants import *
import sys


class ArmMotorControl:

    def __init__(self):
        self.butterHttpClient = ButterConnector(ROBOT_IP).butterHttpClient

    # allows more than one full turn
    def reset_offset(self, motor_name):
        self.butterHttpClient.setMotorRegister(motor_name, 'multi-turn-offset', '0')
    
    # parse response from motor to get position
    def parse_position(self, response):
        try:
            response = response['response']['data']
            return int(response)
        except:
            e = sys.exc_info()[0]
            print("<p>Error: %s</p>" % e)

    # get present position from motor
    def get_present_position(self, motor_name):
        result = self.butterHttpClient.getMotorRegister(motor_name, 'present-position').json()
        print(result)

        while result['executed'] == False:
            result = self.butterHttpClient.getMotorRegister(motor_name, 'present-position').json()
        
        position_str = self.parse_position(result)
        return int(position_str)

    # allow multi-turn and get present position
    def turn_setup(self, motor_name):
        self.reset_offset(motor_name)
        pres_pos = self.get_present_position(motor_name)
        return pres_pos

    # turn clockwise
    def turn_clockwise(self, motor_name, movement=STEP):
        pres_pos = self.turn_setup(motor_name)
        goal_pos = int(pres_pos) + movement
        print(pres_pos, goal_pos)
        self.butterHttpClient.setMotorRegister(motor_name, 'goal-position', str(goal_pos))

    # turn counter-clockwise
    def turn_counter_clockwise(self, motor_name, movement=STEP):
        pres_pos = self.turn_setup(motor_name)
        goal_pos = int(pres_pos) - movement
        self.butterHttpClient.setMotorRegister(motor_name, 'goal-position', str(goal_pos))

    # helper functions to setup next test
    def target_1(self, motor_name):
        goal_pos = int(2245)
        self.butterHttpClient.setMotorRegister(motor_name, 'goal-position', str(goal_pos))
    def target_2(self, motor_name):
        goal_pos = int(1865)
        self.butterHttpClient.setMotorRegister(motor_name, 'goal-position', str(goal_pos))

    # set accelartion and moving speed for KIP
    def set_acceleration(self, motor_name, value):
        self.butterHttpClient.setMotorRegister(motor_name, 'goal-acceleration', str(value))
    def set_moving_speed(self, motor_name, value):
        self.butterHttpClient.setMotorRegister(motor_name, 'moving-speed', str(value))