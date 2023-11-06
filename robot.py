from sr.robot3 import *

import vision
import movement

'''
This script is the one the robot ultimately runs, so load all scripts needed into here

vision.py - Controls Robots camera and marker finding ability - Author Callum R

'''
# -- constants --
robot = Robot()
dev = True # developer mode
power = 0.5

stopping_distance = 150 #mm, distance from marker robot should stop

# -- vision prereq --
current_markers = [] # what markers the robot can currently see
# -- main run loop --
i = 0
while True:
    i += 1
    '''
    Variables:
    movement_values - [angle (in degrees), distance] to nearest marker. If no markers, this is empty
    '''
    movement_values = vision.vision_run(False, dev)
    print(movement_values)
    if i == 5:
        break