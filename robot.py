from sr.robot3 import *

import vision
import movement

'''
This script is the one the robot ultimately runs, so load all scripts needed into here

vision.py - Controls Robots camera and marker finding ability - Author Callum R

'''
# -- constants --
robot = Robot(wait_for_start=False)
dev = True # developer mode
power = 0.5

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
        duration = movement.angle_to_duration(movement_values[0])
