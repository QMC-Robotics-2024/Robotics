"""
In the beginning there was nothing, then there was "behaviour.py"
This script is populated with functions that control the behaviour of our robot
basically all the algorithms and how the robot thinks

Callum Out
"""

import time


def set_motion(parse): # loads the motion file as it is from robot.py
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
    current_markers = [] # array of markers it sees
    while not current_markers:
        scan_time = time.time() + scan_duration # time it moves until
        print("Search Scan")
        while time.time() < scan_time:
            motion.turn_clockwise(robot.motor_boards["SR0GBT"], rotate_power) # move until time
        motion.stop(robot.motor_boards["SR0GBT"]) # stop moving
        check_time = time.time() + check_duration
        """
        put simply there is a maximum time it can check for before moving and checking again
        the next few lines will wait (check duration) amount of time until moving again, if it
        sees anything in this time period, it will break and instead go to that
        """
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
    steps = 7 # used for calculating mean
    distance = int(arudino.command("s")) # get inital distance from ultrasonic sensor
    while distance > sensor_min:# this will permanetly run until our min distanec
        steps_count = []
        motion.forward(motor_board, power)
        for i in range(steps):
            steps_count.append(int(arudino.command("s")))
            # append 5 values to the array
        distance = sum(steps_count) // steps # workout mean distance
        print(distance)
        try:
            values = vision.distance_update(robot, target.id)  # final rotate
            turn_to_marker(motor_board, 0.12 , values[1], 0.005)
            robot.sleep(0.25)
            motion.stop(motor_board)
            motion.forward(motor_board, power)
            print("ARDUINO ROTATE", values[1])  # rotate if can
        except:
            angle = 0  # if it can no longer get data from camera,



def dynamic_speed(distance):
    """
    takes in the distance and returns corresponding motor value
    :param distance:
    :return:
    """
    speed_distance = [[500, 0.25], [800, 0.4], [1200, 0.5], [4000, 0.65], [40000000, 0.7]]  # overflow value
    try:
        for i in range(len(speed_distance)):
            if speed_distance[i][0] <= distance <= speed_distance[i + 1][0]:
                return speed_distance[i][1]
    except IndexError:
        print("Error with distance calculation")
        return 0

def rtb(robot,motor,base,vision,motion,rotate_power):
    '''
    this runs once the block has been collected, and it returns to base
    '''
    base_found = False
    while not base_found:
        seen_markers = robot.camera.see()
        for marker in seen_markers:
            if marker.id in base:
                base_value = marker.id
                base_found = True
                values = vision.distance_update(robot, base_value)
                print(values)
                break
        if base_found:
            break
        motion.turn_clockwise(robot.motor_boards["SR0GBT"], rotate_power-0.2)
        robot.sleep(0.5)
        motion.stop(robot.motor_boards["SR0GBT"])
        robot.sleep(1)
    print(base_value)

    while values[0] > 400:
        turn_to_marker(motor,0.75,values[1],0.00005)
        print("turned")
        drive_to_marker(motor,0.6,values[0],400)
        print("driveded")
        try:
            values = vision.distance_update(robot,base_value)
        except:
            motion.stop(motor)
            robot.sleep(2)
            values=vision.distance_update(robot,base_value)
def position_scan(org_zones, robot, motor):
    '''
    See what position markers we can see.
     ̶A̶v̶e̶r̶a̶g̶e̶ ̶a̶l̶l̶ ̶p̶o̶s̶i̶t̶i̶o̶n̶ ̶I̶D̶'̶s̶ ̶t̶o̶ ̶f̶i̶n̶d̶ ̶g̶e̶n̶e̶r̶a̶l̶ ̶d̶i̶r̶e̶c̶t̶i̶o̶n̶
     Nope that wouldnt work me, what if you can see 27 and 0 you silly bastard
     Okay find which planets we can see the most of their id's?
     what the fuck do it do if it sees equal amounts? - doesnt matter its an array it will go to which it parses first
    Then Move accordingly
    distances = [-3,-2,-1,0,1,2,3]
    middle = [-2]
    mod(middle)
    return pos * mod(middle)
    keep yapping
    like this isnt needed wtf
    '''
    while True:
        current_markers = robot.camera.see()
        if current_markers:
            pos_values = []
            for marker in current_markers:
                if marker.id in range(0, 27):
                    # found a pos marker
                    pos_values.append(marker.id)
            planets_count = []
            for planet in org_zones:
                current_planet_count = sum(id in pos_values for id in planet)
                planets_count.append(current_planet_count)
            most_index = planets_count.index(max(planets_count))
            most_planet = org_zones[most_index]
            print(f"PLANET SEEN: {most_planet}")
            match most_index:
                case 0:
                    drive_to_marker(motor, power=0.4, distance=most_planet.position.distance)
                case 1:
                    # turn left
                    pass
                case 2:
                    pass
                    # turn 180
                case 3:
                    pass
                    # turn right
