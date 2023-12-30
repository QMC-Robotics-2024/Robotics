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
        elif result == -1:  # object is to the left of robot
            motion.turn_anticlockwise(motor_board, rotate_power)
        else:
            motion.stop(motor_board)  # doesnt need to rotate


def drive_to_marker(motor_board, power, distance, min):
    # moves forward to marker
    if distance:
        if distance <= min:
            print("STOP")
            motion.stop(motor_board)
        else:
            motion.forward(motor_board, power)
    else:
        motion.stop(motor_board)

def ultrasonic_drive(motor_board, power, arudino, sensor_min, vision, target, robot):
    """
    This drives the robot at a slower speed using distance from the serial output
    of the arduino, until the distance is at a certain value
    :param motor_board:
    :param power:
    :param arudino:
    :param sensor_min:
    :return:
    """
    steps = 5
    distance = int(arudino.command("s"))
    try:
        values = vision.distance_update(robot, target.id)
        turn_to_marker(motor_board, power + 0.25,values[1],0.001)
        print("ARDUINO ROTATE", values[1])
    except:
        angle = 0
    motion.forward(motor_board, power)
    while distance > sensor_min:
        steps_count = []
        for i in range(steps):
            steps_count.append(int(arudino.command("s")))
        distance = sum(steps_count) // steps
        print(distance)

def dynamic_speed(distance):
    """
    takes in the distance and returns corresponding motor value
    :param distance:
    :return:
    """
    speed_distance = [[500, 0.25], [800, 0.35], [1200, 0.4], [4000, 0.5], [40000000, 0.7]] # overflow value
    try:
        for i in range(len(speed_distance)):
            if speed_distance[i][0] <= distance <= speed_distance[i+1][0]:
                return speed_distance[i][1]
    except IndexError:
        print("Error with distance calculation")
        return 0
