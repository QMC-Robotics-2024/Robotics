from sr.robot3 import *

import vision
import movement
import time
print("Script Running")
'''
This script is the one the robot ultimately runs, so load all scripts needed into here

vision.py - Controls Robots camera and marker finding ability - Author Callum R

'''
# -- constants --
robot = Robot()
dev = True # developer mode

power = 0.5
rotat_power = 0.3
speed = 0 # speed in mps of robot

stopping_distance = 150 #mm, distance from marker robot should stop

scanning_increments = 45 # degrees, if it sees no asterioids, spin this angle and search again
angle_thresh = 2.5# threshold for angle
# -- boards --
motor_board = robot.motor_board
power_board = robot.power_board
robot.power_board.outputs[OUT_H0].is_enabled = True

# -- vision prereq --
current_markers = [] # what markers the robot can currently see
# -- main run loop --

while True:
    '''
    Variables:
    movement_values - [angle (in degrees), distance] to nearest marker. If no markers, this is empty
    '''
    print("Looping..")
    movement_values, target_marker = vision.vision_run(robot, False, dev)
    id = target_marker.id
    if movement_values: # check if not empty
        while True:
            distance, angle = vision.distance_update(robot, id)
            if angle:
                result = movement.rotate_check(angle, angle_thresh)
                if result == 1:
                    movement.turn_clockwise(robot, rotat_power)
                elif result == -1:
                    movement.turn_anticlockwise(robot, rotat_power)
                else:
                    if distance:
                        print("Moving")
                        if distance <= stopping_distance:
                            movement.stop(motor_board)
                            # switch to ultrasonic sensor
                            break
                        else:
                            movement.forward(motor_board, power)
                    else:
                        movement.stop(motor_board)



"""
duration = movement.angle_to_duration(movement_values[0], angle_thresh)
        distance = movement_values[1]
        print(distance)
        if duration != 0: # if rotation needed
            print("Rotating")
            if movement_values[0] > 0:
                time_end = time.time() + duration
                while time.time() < time_end:
                    movement.turn_clockwise(robot, rotat_power)
            else:
                time_end = time.time() + duration
                while time.time() < time_end:
                    movement.turn_anticlockwise(robot, rotat_power)

"""