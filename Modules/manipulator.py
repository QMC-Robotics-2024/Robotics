'''
Program to control the mechanism used for manipulating boxes (Asteroids/Egg)
Program controls suction and raising and lowering of the mechanism

If you have issues with this dm @hackercat77 or tag me on the discord. Odds are something stupid is eff'ed and I need to fix it

Currently waiting for the build team to get their sh*t together so i can finish writing this
(Who in the name of king Charles left bollock put a normal motor on something that requires precise control when there is a box of eff'in servos!!!!)

Author: JP

'''
#----------Imports----------#
# Import student robotics library
from sr.robot3 import *

#----------Subroutines----------#
def suction_on(board, suck_power):
    # Turns on suction
    board.motors[2].power = suck_power
    pass

def suction_off(board):
    # Turns off suction
    board.motors[2].power = 0
    pass

def raise_arm():
    # Raises manipulator mechanism (arm was shorter to type)
    '''
    this will use the servo controller board to raise the arm by a certain factor that will be determined by how high the box needsto be raised
    e.g. to raise high enough to place box in a "spaceship"
    '''
    pass

def lower_arm():
    '''
    Lowers arm (until box is on surface?)
    this will use the servo controler board
    '''
    pass

def rotate_arm(angle_from_robot):
    '''
    rotates arm to desitred position
    this will use the servo controler board
    '''
    pass
    