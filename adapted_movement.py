'''If you have issues with this dm @hackercat77 or tag me on the discord. Odds are something stupid is eff'ed and I need to fix it'''
# Import student robotics library
from sr.robot3 import *

#----------Subroutines----------#
#motor_power_right, motor_power_left
# Power calculation
def calculate_powers(motor_power):
    # This script multiplies the entered motor power by a value to change it by th right percentage to make the motors run at the same speed
    motor_power_right = motor_power
    motor_power_left = motor_power * -0.8

    # Return motor powers
    return motor_power_right, motor_power_left

# Takes angle as an input and returns power and duration
# This might be eff'ed
def angle_to_duration(angle, thresh):
    if angle <= thresh:
        duration = 0
    else:
        duration = angle * (0.85/90)
    return abs(duration)

def rotate_check(angle, thresh):
    if angle >= thresh:
        return 1
    elif angle <= -thresh:
        return -1
    else:
        return 0

# Movement subroutines
# In this implementation, motor powers are pre-flipped to account for mounting arrangement so just stick a "-" infront to reverse direction
def forward(robot, motor_power):
    # Calculate motor powers
    motor_power_right, motor_power_left = calculate_powers(motor_power)

    robot.motor_board.motors[0].power = motor_power_right
    robot.motor_board.motors[1].power = motor_power_left

def reverse(robot, motor_power):
    # Calculate motor powers
    motor_power_right, motor_power_left = calculate_powers(motor_power)

    robot.motor_board.motors[0].power = -motor_power_right
    robot.motor_board.motors[1].power = -motor_power_left

def turn_clockwise(robot, motor_power):
    # Calculate motor powers
    motor_power_right, motor_power_left = calculate_powers(motor_power)

    # Turns clockwise by running the left motor forward and the right motor backward
    robot.motor_board.motors[0].power = -motor_power_right
    robot.motor_board.motors[1].power = motor_power_left

def turn_anticlockwise(robot, motor_power):
    # Calculate motor powers
    motor_power_right, motor_power_left = calculate_powers(motor_power)

    # Turns clockwise by running the left motor backward and the right motor forward
    robot.motor_board.motors[0].power = motor_power_right
    robot.motor_board.motors[1].power = -motor_power_left

def stop_motors(robot):
    # Stops motors
    # BRAKE is equivilant to setting power to 0
    robot.motor_board.motors[0].power = BRAKE
    robot.motor_board.motors[1].power = BRAKE
