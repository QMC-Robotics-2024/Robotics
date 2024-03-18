from sr.robot3 import *

from Modules import vision
from Modules import adapted_movement as motion
from Modules import manipulator as arm
from Modules import behaviour
from Modules import position
print("Script Running")
'''
This script is the one the robot ultimately runs, so load all scripts needed into here

vision.py - Controls Robots camera and marker finding ability - Author Callum R

'''
# -- constants --
dev = True# developer mode
dev_zone = 0

power = 0.7
rotat_power = 0.7

stopping_distance = 800  # mm, distance from marker robot should stop and switch to ultrasonic

angle_thresh = 0.005 # threshold for angle

scan_duration = 0.5  # how long it turns for when scanning
check_duration = 0.4  # how long it checks for
rotate_increment_speed = 0.3

arduino_speed = 0.2
arduino_min = 400 # distance in mm arduino stops robot

# -- boards --
robot = Robot()

power_board = robot.power_board
robot.power_board.outputs[OUT_H0].is_enabled = True

motor_board = robot.motor_board

# Use these when arm control is needed
#motor_board = robot.motor_boards["placeholderSerialAddress1"]
#arm_motor_board = robot.motor_boards["placeholderSerialAddress2"]

arduino = robot.arduino # using extended SR firmware (no reason really tbh)

mode = robot.mode
if mode == "COMP":
    zone = robot.zone
else:
    zone = dev_zone
base = position.zone_parse(zone) # give our zone to robot

# -- vision prereq --
current_markers = []  # what markers the robot can currently see
# -- main run loop --
behaviour.set_motion(motion) # parse the motion script to behaviour
while True:
    '''
    Variables:
    movement_values - [angle (in degrees), distance] to nearest marker. If no markers, this is empty
    '''
    try:
        movement_values, target_marker, current_markers = vision.vision_run(robot, False, dev)
        id = target_marker.id
    except TypeError:
        movement_values = []
    if movement_values:
        print("Inital Values Stated")  # check if not empty
        while True:
            distance = 0
            angle = 0
            try:
                # try finding the distance, if it cant see it, set distance and angle to 0
                distance, angle = vision.distance_update(robot, id)
                print(f"Distance Updated: distance [{distance}], angle [{angle}]")
            except TypeError:
                # this stops it if it cant find any asteroids, so it can search without blur
                print("No Values Found")
            if not distance and not angle:
                print("Starting Check")
                motion.stop(motor_board)
                robot.sleep(check_duration)
                try:
                    distance, angle = vision.distance_update(robot, id)
                    print("Values found from check")
                except TypeError:
                    # it can no longer find the marker, so update it
                    print("Lost Marker, Updating")
                    try:
                        movement_values, target_marker, current_markers = vision.vision_run(robot, False, dev)
                        distance, angle = vision.distance_update(robot, target_marker.id)
                    except TypeError:
                        print("Beginning Scan")
                        power = 0.5
                        rotat_power = 0.7
                        current_markers = False
                        while not current_markers:
                            print("Scanning")
                            current_markers = behaviour.scan_for_markers(robot, rotate_increment_speed, scan_duration,
                                                                         check_duration)
                        movement_values, target_marker, current_markers = vision.vision_run(robot, False, dev)
                        id = target_marker.id
                        distance, angle = vision.distance_update(robot, id)
                        print("Found Values")
            if distance > stopping_distance:
                power = behaviour.dynamic_speed(distance)
                rotat_power = power + 0.25
                behaviour.turn_to_marker(motor_board, rotat_power, angle, angle_thresh)
                behaviour.drive_to_marker(motor_board, power, distance, stopping_distance)
            elif distance == stopping_distance or distance < stopping_distance:
                print("[ARDUINO ACTIVE]")
                behaviour.ultrasonic_drive(motor_board, arduino_speed, arduino, arduino_min, vision, target_marker, robot)
                motion.stop(motor_board)
                print("MARKER STOP RUN COLLECT PROCEUDRE")
            else:
                motion.stop(motor_board)
    elif not movement_values:
        while not current_markers:
            print("None Seen")
            current_markers = behaviour.scan_for_markers(robot, rotate_increment_speed, scan_duration, check_duration)

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
