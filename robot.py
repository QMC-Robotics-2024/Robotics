from sr.robot3 import *

import vision
import movement
import time
'''
This script is the one the robot ultimately runs, so load all scripts needed into here

vision.py - Controls Robots camera and marker finding ability - Author Callum R

'''
# -- constants --
robot = Robot(wait_for_start=False)
dev = True # developer mode

power = 0.5
speed = 0 # speed in mps of robot

stopping_distance = 150 #mm, distance from marker robot should stop
angle_thresh = 1 # threshold for angle
# -- boards --
motor_board = robot.motor_board
power_board = robot.power_board
robot.power_board.outputs[OUT_H0].is_enabled = True

# -- vision prereq --
current_markers = [] # what markers the robot can currently see
# -- main run loop --

while True:
    robot.wait_start()
    '''
    Variables:
    movement_values - [angle (in degrees), distance] to nearest marker. If no markers, this is empty
    '''
    movement_values = vision.vision_run(robot, False, dev)
    if movement_values: # check if not empty
        duration = movement.angle_to_duration(movement_values[0], angle_thresh)
        if duration != 0: # if rotation needed
            if movement_values[0] > 0:
                time_end = time.time() + duration
                while time.time() < time_end:
                    movement.turn_clockwise(robot, power)
            else:
                time_end = time.time() + duration
                while time.time() < time_end:
                    movement.turn_anticlockwise(robot, power)
        movement.forward(motor_board, power)


