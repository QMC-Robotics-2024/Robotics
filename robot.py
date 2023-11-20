from sr.robot3 import *

import vision
#import movement #obselete as movesd to new movement system
import adapted_movement as motion
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
rotation_power = 0.1
speed = 0 # speed in mps of robot

stopping_distance = 150 #mm, distance from marker robot should stop

scanning_increments = 45 # degrees, if it sees no asterioids, spin this angle and search again
angle_thresh = 0.05# threshold for angle

exposure_values = [x for x in range(-13, 0)] # camera settings

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
    # get inital values
    movement_values, target_marker = vision.vision_run(robot, False, dev)
    id = target_marker.id
    if movement_values: # check if not empty
        while True:
            try:
                # try finding the distance, if it cant see it, set distance and angle to 0
                distance, angle = vision.distance_update(robot, id)
            except:
                # this stops it if it cant find any asteroids, so it can search without blur
                distance = 0
                angle = 0
            if angle: # if there is any value for angle
                result = motion.rotate_check(angle, angle_thresh) # checks if the angle is above/below threshold

                if result == 1: # object is to the right of robot
                    # Rotates clockwise to try and face object
                    motion.turn_clockwise(robot, rotation_power)
                    print("Rotate")
                elif result == -1: # object is to the left of robot
                    # Rotates anticlockwise to try and face object
                    motion.turn_anticlockwise(robot, rotation_power)
                    print("Rotate")
                else:
                    # Stop motors
                    motion.stop_motors(motor_board) # doesnt need to rotate
            if distance: # not an elsif so it wont be skipped
                if distance <= stopping_distance:
                    motion.stop_motors(motor_board)
                    # switch to ultrasonic sensor
                    break
                else:
                    # Has robot move forward
                    motion.forward(motor_board, power)        
            else:
                # Stop moving
                motion.stop_motors(motor_board)


"""
duration = movement.angle_to_duration(movement_values[0], angle_thresh)
        distance = movement_values[1]
        print(distance)
        if duration != 0: # if rotation needed
            print("Rotating")
            if movement_values[0] > 0:
                time_end = time.time() + duration
                while time.time() < time_end:
                    movement.turn_clockwise(motor_board, rotation_power)
            else:
                time_end = time.time() + duration
                while time.time() < time_end:
                    movement.turn_anticlockwise(motor_board, rotation_power)

"""
