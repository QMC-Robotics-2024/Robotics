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
#robot.activateFreakMode()

# -- constants --
dev = True  # developer mode
dev_zone = 0

power = 0.9
rotat_power = 0.95

stopping_distance = 500  # mm, distance from marker robot should stop and switch to ultrasonic

angle_thresh = 0.0000005  # threshold for angle

scan_duration = 0.5  # how long it turns for when scanning
check_duration = 0.35  # how long it checks for
rotate_increment_speed = 0.5

arduino_speed = 0.4
arduino_min = 70  # distance in mm arduino stops robot
arduino_timeout = 12 # max time arduino can be used before stopping
# -- boards --
robot = Robot()
motor_board = robot.motor_boards["SR0GBT"]
arm_board = robot.motor_boards["SR0RG1U"]
power_board = robot.power_board
robot.power_board.outputs[OUT_H0].is_enabled = True
arduino = robot.arduino  # using extended SR firmware (no reason really tbh)
current_markers = []
mode = robot.mode
'''
if mode == "COMP":
    zone = robot.zone
else:
    zone = dev_zone
    '''
zone = robot.zone
base, spaceship = position.zone_parse(zone)  # give our zone  id's to robot

# -- main run loop --
behaviour.set_motion(motion)
# parse the motion script to behaviour
manipulator.raise_arm(arm_board, 0.6)
manipulator.open_gripper(arm_board, 0.45)
robot.sleep(1.2)
manipulator.stop_gripper(arm_board)
manipulator.stop_arm(arm_board)

include = [x for x in range(149, 200)]
# reset gripper
while True:
    try:
        # inital search for a marker
        movement_values, target_marker, current_markers = vision.vision_run(robot, include, False, dev)
        id = target_marker.id
    except TypeError:  # if no markers found set the values to empty
        movement_values = []
    if movement_values:
        print(f"Found Values For Marker ID: {id}")  # check if not empty
        while True:
            distance = 0  # so dont move
            angle = 0
            try:
                # try finding the distance, if it cant see it, set distance and angle to 0
                distance, angle = vision.distance_update(robot, id)
                print(f"Distance Updated: distance [{distance}], angle [{angle}]")
            except TypeError:
                motion.stop(motor_board)
                # this stops it if it cant find any asteroids, so it can search without blur
                print(f"Lost Marker: {id}")
            if not distance and not angle:  # if none found start spinning and search
                print(f"[{id}] Retrying Marker")
                motion.stop(motor_board)
                robot.sleep(check_duration)
                try:
                    distance, angle = vision.distance_update(robot, id)  # if it can update GREAT
                    print(f"[{id}] Values found from check")
                except TypeError:
                    # it can no longer find the marker, so update it
                    print(f"[{id}] Lost Marker, Final Check")
                    try:
                        movement_values, target_marker, current_markers = vision.vision_run(robot, include, False, dev)
                        distance, angle = vision.distance_update(robot, target_marker.id)  # try one last time
                    except TypeError:  # cant see any so start scanning
                        print(f"Lost Marker [{id}]")
                        print(" " * 10)
                        print("Scanning for new markers")
                        current_markers = False
                        while not current_markers:
                            print("Scanning...")
                            current_markers = behaviour.scan_for_markers(robot, rotate_increment_speed, scan_duration,
                                                                         check_duration)
                        try:
                            movement_values, target_marker, current_markers = vision.vision_run(robot, include, False, dev)
                            id = target_marker.id
                            distance, angle = vision.distance_update(robot, id)
                            print(f"Found Marker: {id}")
                        except:
                            pass
            if distance > stopping_distance:
                power = behaviour.dynamic_speed(distance)
                if angle > 10 * (3.14159265) / 180:  # if the angle is too great, stop moving
                    print("f[{id}] Angle too great, initaiting turn")
                    motion.stop(motor_board)
                    behaviour.turn_to_marker(motor_board, 0.2, angle, angle_thresh)
                else:
                    print(f"[{id}] Distance: {distance}, Angle: {angle}")
                    behaviour.turn_to_marker(motor_board, rotat_power, angle, angle_thresh)
                    behaviour.drive_to_marker(motor_board, power, distance, stopping_distance)
            elif distance <= stopping_distance:
                print("[ARDUINO ACTIVE]")
                check2 = behaviour.ultrasonic_drive(motor_board, arduino_speed, arduino, arduino_min, vision, target_marker,
                                           robot, arduino_timeout)
                # move until positioned well
                if not check2:
                    continue
                print("*" * 15)
                print("[ARM] Iniating Pickup Procedure")
                motion.stop(motor_board)  # in position
                manipulator.lower_arm(arm_board, 0.7)  # lower de arm
                robot.sleep(1)
                print("arm in position")
                manipulator.stop_arm(arm_board)
                robot.sleep(0.5)
                print("closing grip")
                manipulator.close_gripper(arm_board, 0.7)
                robot.sleep(1.9)
                manipulator.stop_gripper(arm_board)
                robot.sleep(1)
                print("raising arm")
                manipulator.raise_arm(arm_board, 0.8)
                robot.sleep(2)
                manipulator.stop_arm(arm_board)
                check = behaviour.check_switch(arduino)
                if check:
                    pass
                elif not check:
                    motion.reverse(motor_board, power)
                    manipulator.open_gripper(arm_board, 0.5)
                    robot.sleep(0.8)
                    manipulator.stop_gripper(arm_board)
                    continue
                print("Ready To RTB")
                behaviour.rtb_updated(robot, motor_board, base, vision, motion, rotat_power)
                motion.stop(motor_board)
                robot.sleep(1)
                try:
                    for i in range(0,5):
                        motion.turn_anticlockwise(motor_board, rotat_power - 0.15)
                        robot.sleep(0.2)
                        motion.stop(motor_board)
                        print("Can I see Spaceship")
                        robot.sleep(1)
                        try:
                            movement_values, target_marker, current_markers = vision.vision_run(robot, spaceship, False,
                                                                                                dev)
                            if target_marker.id in spaceship:
                                print("Can see it")
                                break
                        except:
                            pass

                    if target_marker.id in spaceship:
                        include.remove(id)
                        tmp = 0.5
                        print("I can") # if it can see the ship, assume it places it in there, and ignore that block
                        distance, angle = vision.distance_update(robot, target_marker.id)
                        while distance > 10:
                            print("drive")
                            if distance < 70:
                                tmp = 0.3
                            behaviour.turn_to_marker(motor_board,rotat_power,angle,0.000005)
                            behaviour.drive_to_marker(motor_board,tmp,distance,25)
                            try:
                                distance, angle = vision.distance_update(robot, target_marker.id)
                                if distance:
                                    pass
                            except:
                                motion.stop(motor_board)
                                distance = 0
                                motion.turn_clockwise(motor_board,0.2)
                                robot.sleep(0.3)
                                motion.stop(motor_board)

                except:
                    pass
                manipulator.lower_arm(arm_board,0.5)
                robot.sleep(1)
                manipulator.stop_arm(arm_board)
                manipulator.open_gripper(arm_board, 0.7)
                robot.sleep(0.4)
                manipulator.stop_gripper(arm_board)
                manipulator.raise_arm(arm_board,0.7)
                robot.sleep(1)
                manipulator.stop_arm(arm_board)
                motion.reverse(motor_board, 0.6)
                robot.sleep(1)
                motion.stop(motor_board)
                motion.turn_anticlockwise(motor_board, 0.5)
                robot.sleep(0.7)
                motion.stop(motor_board)
                print("Next Box")

                '''
                motion.stop(motor_board)
                manipulator.open_gripper(arm_board,0.7)
                manipulator.lower_arm(arm_board,0.5)
                print("Asteroid Dumped")
                motion.turn_clockwise(motor_board, 0.5)
                robot.sleep(1)
                manipulator.stop_gripper(arm_board)
                manipulator.stop_arm(arm_board)
                motion.turn_clockwise(motor_board, 0.5)
                motion.forward(motor_board,0.7)
                robot.sleep(0.4)
                motion.stop(motor_board)
                manipulator.raise_arm(arm_board,0.7)
                robot.sleep(1)
                manipulator.stop_arm(arm_board)
                print("NEXT BOX")
                '''
            else:
                motion.stop(motor_board)
    elif not movement_values:
        while not current_markers:
            print("No Markers in sight, scanning")
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


# SR0GBT
# SR0RG1U
