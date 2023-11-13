#----------Imports----------#
# Import student robotics library
from sr.robot3 import *
import time
#----------Variable definitions----------#
# Constants 
# All numbers in variable names relate to which port the device is connected to
motor_power_right = -0.45
motor_power_left = 0.5
duration = 2.3
duration2 = 2.9
turn_duration = 0.55 
turn_duration2 = 1.3  # 0.65 90 degrees  roughly, 1.25 180 degrees roughly 
stop_duration = 0.25
#----------Setup----------#
# Define robot
robot = Robot()

# Define motor board
motor_board = robot.motor_board

# Define powerboard
power_board = robot.power_board

# Enable port 0 on powerboard
robot.power_board.outputs[OUT_H0].is_enabled = True

#----------Subroutines----------#
# Movement subroutines
# In this implementation, motor powers are predefined so just stick a - infrount to reverse direction
def move_forward(motor_power_right, motor_power_left, duration):
    robot.motor_board.motors[0].power = motor_power_right
    robot.motor_board.motors[1].power = motor_power_left
    time.sleep(duration)
    stop_motors()
def move_forward2(motor_power_right, motor_power_left):
    robot.motor_board.motors[0].power = motor_power_right
    robot.motor_board.motors[1].power = motor_power_left
    time.sleep(1.6)
    stop_motors()
def move_backward(motor_power_right, motor_power_left, duration):
    robot.motor_board.motors[0].power = -motor_power_right
    robot.motor_board.motors[1].power = -motor_power_left
    time.sleep(duration)
    stop_motors()
def turn_clockwise(motor_power_right, motor_power_left, duration):
    # Turns clockwise by running the left motor forward and the right motor backward
    robot.motor_board.motors[0].power = -motor_power_right
    robot.motor_board.motors[1].power = motor_power_left
    time.sleep(turn_duration)
    stop_motors()
def turn_anticlockwise(motor_power_right, motor_power_left, duration):
    #Turns clockwise by running the left motor backward and the right motor forward
    robot.motor_board.motors[0].power = motor_power_right
    robot.motor_board.motors[1].power = -motor_power_left
    time.sleep(turn_duration)
    stop_motors()
def turn_clockwise2(motor_power_right, motor_power_left):
    # Turns clockwise by running the left motor forward and the right motor backward
    robot.motor_board.motors[0].power = -motor_power_right
    robot.motor_board.motors[1].power = motor_power_left
    time.sleep(0.6)# to much maybe 0.8
    stop_motors()
def stop_motors():
    # Stops motors
    # BREAK is equivilant to setting power to 0
    robot.motor_board.motors[0].power = BRAKE
    robot.motor_board.motors[1].power = BRAKE
    time.sleep(stop_duration)
#----------Subroutines----------#
move_forward(motor_power_right, motor_power_left, duration) #working
turn_clockwise(motor_power_right, motor_power_left, turn_duration)   #working 
move_forward(motor_power_right, motor_power_left, duration2) #working 
turn_clockwise2(motor_power_right, motor_power_left)   #working 
move_forward2(motor_power_right, motor_power_left) #working
turn_clockwise2(motor_power_right, motor_power_left)   #working
move_forward(motor_power_right, motor_power_left, duration2) #working 
#move_forward(motor_power_right, motor_power_left, duration) #working
#turn_clockwise(motor_power_right, motor_power_left, turn_duration2)   #working 
#move_forward(motor_power_right, motor_power_left, duration2) #working
robot.sleep(1)
#move_forward(motor_power_right, motor_power_left, duration) #working
#move_backward(motor_power_right, motor_power_left, duration) #working
#turn_anticlockwise(motor_power_right, motor_power_left, duration)   #working 
#turn_clockwise(motor_power_right, motor_power_left, duration) #working