from sr.robot3 import *

import vision
'''
This script is the one the robot ultimately runs, so load all scripts needed into here

vision.py - Controls Robots camera and marker finding ability - Author Callum R

'''
# -- constants --
robot = Robot()
current_markers = [] # what markers the robot can currently see

stopping_distance = 150 #mm, distance from marker robot should stop

# -- main run loop --
while True:
    '''
    Variables:
    movement_values - [angle (in degrees), distance] to nearest marker. If no markers, this is empty
    '''
    movement_values = vision.vision_run()
    if movement_values:
        # robot_turn(movment_values[0])
        # vision.check_if_centre()
        # robot_forward(movment_values[1] - stopping_distance)
