'''
Program to control the mechanism used for manipulating boxes (Asteroids/Egg)
Program controls suction and raising and lowering of the mechanism

If this eff's itself in during the competition someone else will have to fix it as I'll be on an Egyptian beach drinking cocktails


Author: JP

Syntax:
arm.subroutine(arm_motor_board, power)

'''
#----------Imports----------#
# Import student robotics library
from sr.robot3 import *

#----------Subroutines----------#
def raise_arm(board, arm_power):
    board.motors[0].power = arm_power

def lower_arm(board, arm_power):
    board.motors[0].power = -arm_power

def open_gripper(board, grip_power):
    board.motors[0].power = grip_power

def close_gripper(board, grip_power):
    board.motors[0].power = -grip_power