from sr.robot3 import *

'''
** Useful values **

 Forward -> [negative, positive]
 Reverse -> [positive, negative]
 
 90 deg turn -> 0.5 power 0.65 duration
'''


# takes angle as an input and returns power and duration
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

# need to be modified once the distance-power conversion is found
def forward(board, power=0.5):
    board.motors[0].power = -power
    board.motors[1].power = power


def reverse(board, power=0.5):
    board.motors[0].power = power
    board.motors[1].power = -power

def turn_clockwise(board, power=0.5): # adapted from Jack's script
    board.motors[0].power = -power
    board.motors[1].power = -power
def turn_anticlockwise(board, power=0.5):
    board.motors[0].power = power
    board.motors[1].power = power

def stop(board):
    board.motors[0].power = 0
    board.motors[1].power = 0


