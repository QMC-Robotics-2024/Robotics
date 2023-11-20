import cv2
from sr.robot3 import *
import cv2 as cv
import numpy as np

def dynamic_exposure_test():
    exposure_values = [x for x in range(-13, 0)] # camera exposure range

    robot = Robot()
    cap = cv.VideoCapture(0) # set camera
    for value in exposure_values: # for every camera exposure setting
        cap.set(cv.CAP_PROP_EXPOSURE, value) # set this exposure
        res, frame = cap.read() # read the frame (comes with res seperate)
        markers = robot.camera.see(frame) # find markers
        if markers: # if it can see
            target_marker = markers[0]
            corners = target_marker.pixel_corners # get values
            points = np.array(points, np.int32)
            points = points.reshape((-1,1,2)) # these just sort values for open-cv
            cv.polylines(frame, [points], True, (0,255,0)) # draw the shape
            cv.imwrite(f"{value}_exposure_True", frame) # save this image
        else:
            cv.imwrite(f"f{value}_exposure_False", frame) # save this image


def set_dynamic_exposure(cap, exposure_values, robot, offset=1):
    '''

    :param cap, exposure_values, robot, offset:
    :return: exposure_value

    This takes a bunch of photos and adjusts the exposure to attempt to find the minimum exposure
    setting, adding an offset for caution. This can be ran multiple times if there is an issue
    '''
    working_values = []
    for value in exposure_values:  # for every camera exposure setting
        cap.set(cv.CAP_PROP_EXPOSURE, value)  # set this exposure
        res, frame = cap.read()  # read the frame (comes with res seperate)
        markers = robot.camera.see(frame)  # find markers
        if markers:  # if it can see
            working_values.append(value)
        else:
            pass # it cant see it
    working_values.sort()
    return (working_values[0] + offset)