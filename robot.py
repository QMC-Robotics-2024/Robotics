from sr.robot3 import *

from Modules import vision
from Modules import adapted_movement as motion
from Modules import behaviour
from Modules import position
from Modules import manipulator

print("Script Running")
'''
This script is the one the robot ultimately runs, so load all scripts needed into here

vision.py - Controls Robots camera and marker finding ability - Author Callum R
position.py - info about pos -
behaviour.py - ltitteraly everything 

'''
# -- constants --
dev = True  # developer mode
dev_zone = 0

power = 0.8
rotat_power = 0.85

stopping_distance = 800  # mm, distance from marker robot should stop and switch to ultrasonic

angle_thresh = 0.00005  # threshold for angle

scan_duration = 0.5  # how long it turns for when scanning
check_duration = 0.35  # how long it checks for
rotate_increment_speed = 0.5

arduino_speed = 0.4
arduino_min = 400  # distance in mm arduino stops robot
# -- boards --
robot = Robot()
motor_board = robot.motor_boards["SR0GBT"]
arm_board = robot.motor_boards["SR0RG1U"]
power_board = robot.power_board
robot.power_board.outputs[OUT_H0].is_enabled = True
arduino = robot.arduino  # using extended SR firmware (no reason really tbh)

mode = robot.mode
if mode == "COMP":
    zone = robot.zone
else:
    zone = dev_zone
base = position.zone_parse(zone)  # give our zone to robot

# -- main run loop --
behaviour.set_motion(motion)  # parse the motion script to behaviour
while True:
    try:
        # inital search for a marker
        movement_values, target_marker, current_markers = vision.vision_run(robot, False, dev)
        id = target_marker.id
    except TypeError: # if no markers found set the values to empty
        movement_values = []
    if movement_values:
        print("Inital Values Stated")  # check if not empty
        while True:
            distance = 0 # so dont move
            angle = 0
            try:
                # try finding the distance, if it cant see it, set distance and angle to 0
                distance, angle = vision.distance_update(robot, id)
                print(f"Distance Updated: distance [{distance}], angle [{angle}]")
            except TypeError:
                motion.stop(motor_board)
                # this stops it if it cant find any asteroids, so it can search without blur
                print("No Values Found")
            if not distance and not angle: # if none found start spinning and search
                print("Starting Check")
                motion.stop(motor_board)
                robot.sleep(check_duration)
                try:
                    distance, angle = vision.distance_update(robot, id) # if it can update GREAT
                    print("Values found from check")
                except TypeError:
                    # it can no longer find the marker, so update it
                    print("Lost Marker, Updating")
                    try:
                        movement_values, target_marker, current_markers = vision.vision_run(robot, False, dev)
                        distance, angle = vision.distance_update(robot, target_marker.id) # try one last time
                    except TypeError: # cant see any so start scanning
                        print("Beginning Scan")
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
                if angle > 5 * (3.14159) / 180: # if the angle is too great, stop moving
                    motion.stop(motor_board)
                    behaviour.turn_to_marker(motor_board, 0.25, angle, angle_thresh)
                else:
                    behaviour.turn_to_marker(motor_board, rotat_power, angle, angle_thresh)
                    behaviour.drive_to_marker(motor_board, power, distance, stopping_distance)
            elif distance == stopping_distance or distance < stopping_distance:
                print("[ARDUINO ACTIVE]")
                behaviour.ultrasonic_drive(motor_board, arduino_speed, arduino, arduino_min, vision, target_marker,
                                           robot) # move until positioned well
                motion.stop(motor_board) # in position
                manipulator.lower_arm(arm_board,0.3) # lower de arm
                robot.sleep(1)
                manipulator.stop_arm(arm_board)
                manipulator.close_gripper(arm_board,0.3)
                robot.sleep(1)
                break
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

#SR0GBT
#SR0RG1U
