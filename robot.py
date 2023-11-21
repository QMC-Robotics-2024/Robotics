from sr.robot3 import *

from Modules import vision
from Modules import movement as motion
from Modules import behaviour

print("Script Running")
'''
This script is the one the robot ultimately runs, so load all scripts needed into here

vision.py - Controls Robots camera and marker finding ability - Author Callum R

'''
# -- constants --
robot = Robot()
dev = True # developer mode

power = 0.5
rotat_power = 0.2
speed = 0 # speed in mps of robot

stopping_distance = 500 #mm, distance from marker robot should stop


angle_thresh = 0.05# threshold for angle

exposure_values = [x for x in range(-13, 0)] # camera settings

scan_duration = 1 # how long it turns for when scanning
check_duration = 2 # how long it checks for
rotate_incremen_speed = 0.5

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
    movement_values, target_marker, current_markers = vision.vision_run(robot, False, dev)
    id = target_marker.id
    if movement_values: # check if not empty
        while True:
            distance = 0
            angle = 0
            try:
                # try finding the distance, if it cant see it, set distance and angle to 0
                distance, angle = vision.distance_update(robot, id)
            except:
                # this stops it if it cant find any asteroids, so it can search without blur
                pass
            if not distance and not angle:
                robot.sleep(check_duration)
                try:
                    distance, angle = vision.distance_update(robot, id)
                except:
                    # it can no longer find the marker, so update it
                    movement_values, target_marker, current_markers = vision.vision_run(robot, False, dev)
                    while not current_markers:
                        current_markers = behaviour.scan_for_markers(robot, rotate_incremen_speed, scan_duration, check_duration)
                    movement_values, target_marker, current_markers = vision.vision_run(robot, False, dev)
                    id = target_marker.id
                    distance, angle = vision.distance_update(robot, id)
            behaviour.turn_to_marker(motor_board, rotat_power, angle, angle_thresh)
            behaviour.drive_to_marker(motor_board, power, distance, stopping_distance)


"""
duration = movement.angle_to_duration(movement_values[0], angle_thresh)
        distance = movement_values[1]
        print(distance)
        if duration != 0: # if rotation needed
            print("Rotating")
            if movement_values[0] > 0:
                time_end = time.time() + duration
                while time.time() < time_end:
                    movement.turn_clockwise(motor_board, rotat_power)
            else:
                time_end = time.time() + duration
                while time.time() < time_end:
                    movement.turn_anticlockwise(motor_board, rotat_power)

"""
