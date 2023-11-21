'''
In the beginning there was nothing, then there was "behaviour.py"
This script is populated with functions that control the behaviour of our robot
basically all the algorithims and how the robot thinks

Callum Out
'''
import movement as motion
import vision

import time

def scan_for_markers(robot, rotate_power, scan_duration, check_duration):
    """
    :param robot:
    :param rotate_power:
    :param scan_duration:
    :param check_duration:
    :return:

    So this script runs if there are no markers present, it will rotate for
    a set amount of time then scan for any markers present for a given time
    if there isnt any, itll just re-run the loop and rotate again.
    """
    current_markers = []
    while not current_markers:
        scan_time = time.time() + scan_duration
        while time.time() < scan_time:
            motion.turn_clockwise(robot, rotate_power)
        motion.stop(robot.motor_board)
        check_time = time.time() + check_duration
        while time.time() < check_time:
            current_markers = robot.camera.see()
    return  current_markers

def turn_to_marker(motor_board, rotate_power, angle, angle_thresh):
    if angle:  # if there is any value for angle
        result = motion.rotate_check(angle, angle_thresh)  # checks if the angle is above/below threshold
        if result == 1:  # object is to the right of robot
            motion.turn_clockwise(motor_board, rotate_power)
        elif result == -1:  # object is to the left of robot
            motion.turn_anticlockwise(motor_board, rotate_power)
        else:
            motion.stop(motor_board)  # doesnt need to rotate
def drive_to_marker(motor_board,power,distance, min):
    # moves forward to marker
    if distance:
        if distance <= min:
            motion.stop(motor_board)
        else:
            motion.forward(motor_board, power)
    else:
        motion.stop(motor_board)

