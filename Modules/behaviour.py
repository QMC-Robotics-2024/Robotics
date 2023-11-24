"""
In the beginning there was nothing, then there was "behaviour.py"
This script is populated with functions that control the behaviour of our robot
basically all the algorithims and how the robot thinks

Callum Out
"""

import time


def set_motion(parse):
    global motion
    motion = parse


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
        print("Search Scan")
        while time.time() < scan_time:
            motion.turn_clockwise(robot.motor_board, rotate_power)
        motion.stop(robot.motor_board)
        check_time = time.time() + check_duration
        print("Waiting...")
        while time.time() < check_time:
            current_markers = robot.camera.see()
            if current_markers:
                break
    return current_markers


def turn_to_marker(motor_board, rotate_power, angle, angle_thresh):
    if angle:  # if there is any value for angle
        result = motion.rotate_check(angle, angle_thresh)  # checks if the angle is above/below threshold
        if result == 1:  # object is to the right of robot
            motion.turn_clockwise(motor_board, rotate_power)
            print("Turning Clockwise")
        elif result == -1:  # object is to the left of robot
            motion.turn_anticlockwise(motor_board, rotate_power)
            print("Turning Anticlockwise")
        else:
            motion.stop(motor_board)  # doesnt need to rotate


def drive_to_marker(motor_board, power, distance, min):
    # moves forward to marker
    if distance:
        print("Distance Still")
        if distance <= min:
            print("STOP")
            motion.stop(motor_board)
        else:
            motion.forward(motor_board, power)
    else:
        motion.stop(motor_board)

def ultrasonic_drive(motor_board, power, arudino, sensor_min):
    """
    This drives the robot at a slower speed using distance from the serial output
    of the arduino, until the distance is at a certain value
    :param motor_board:
    :param power:
    :param arudino:
    :param sensor_min:
    :return:
    """
    distance = arudino.command('s')
    motion.forward(motor_board, power)
    while distance > sensor_min:
        distance = arudino.command("s")
    motion.stop(motor_board)