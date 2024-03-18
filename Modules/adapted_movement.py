'''
This program controls all major movement functions of the robot

If this eff's itself in during the competition someone else will have to fix it as I'll be on an Egyptian beach drinking cocktails

Author: JP
'''
# Import student robotics library
from sr.robot3 import *

#----------Subroutines----------#
#motor_power_right, motor_power_left
# Power calculation
def calculate_powers(motor_power):
    # This script multiplies the entered motor power by a value to change it by th right percentage to make the motors run at the same speed
    motor_power_right = motor_power*-1
    motor_power_left = motor_power * 0.9            #0.8 worked well on the test platform

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


def rotate_check(angle, thresh) -> int:
    """
    This checks whether the robot needs to turn or not
    :param angle: the horizontal angle to the block
    :param thresh: the uncertainty in the angle
    1: it is to the right
    -1: it is to the left
    0: it is within the threshold
    """
    if angle >= thresh:
        return 1
    elif angle <= -thresh:
        return -1
    else:
        return 0


# Movement subroutines
# In this implementation, motor powers are pre-flipped to account for mounting arrangement so just stick a "-" infront to reverse direction
def forward(board, motor_power):
    # Calculate motor powers
    motor_power_right, motor_power_left = calculate_powers(motor_power)

    board.motors[0].power = motor_power_right
    board.motors[1].power = motor_power_left


def reverse(board, motor_power):
    # Calculate motor powers
    motor_power_right, motor_power_left = calculate_powers(motor_power)

    board.motors[0].power = -motor_power_right
    board.motors[1].power = -motor_power_left


def turn_anticlockwise(board, motor_power):
    # Calculate motor powers
    motor_power_right, motor_power_left = calculate_powers(motor_power)

    # Turns clockwise by running the left motor forward and the right motor backward
    board.motors[0].power = motor_power_right
    board.motors[1].power = -motor_power_left


def turn_clockwise(board, motor_power):
    # Calculate motor powers
    motor_power_right, motor_power_left = calculate_powers(motor_power)

    # Turns clockwise by running the left motor backward and the right motor forward
    board.motors[0].power = -motor_power_right
    board.motors[1].power = motor_power_left


def stop(board):
    # Stops motors
    # BRAKE is equivilant to setting power to 0
    board.motors[0].power = 0
    board.motors[1].power = 0
