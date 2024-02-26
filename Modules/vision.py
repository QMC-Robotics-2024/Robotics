import sr.robot3
import cv2 as cv
import math

'''
Assumptions I am making:

- Different processes/thread
- Robot goes for closest marker (asteroid) first
'''


# ini
# this function runs first to initally find an asteroid, and returns the closest asteroid
def vision_run(robot, save=False, dev=False):
    if not dev:
        # cv2 will allow us to adjust image info and make manipulations such as contrast if needed
        frame = robot.camera.capture()
        # run frame checks and manipulations etc
        markers = robot.camera.see(frame)
    else:  # capture doesnt work in simulation
        markers = robot.camera.see()

    current_markers = markers
    if not markers:
        current_markers.clear()
        return False
    elif markers:
        target_marker = marker_sort(current_markers)
        move_values = movement_calculate(target_marker)
        return move_values, target_marker, current_markers


def marker_sort(current_markers):
    # sort markers by distance,
    sorted_markers = []
    for marker in current_markers:
        if marker.id not in [i for i in range(0,29)]:
            position = markerpos(marker)
            sorted_markers.append(position)
    sorted(sorted_markers, key=lambda x: x[3])  # element at index 3 is distance
    target_marker = current_markers[current_markers.index(sorted_markers[0][0])]
    return target_marker


def markerpos(marker):
    # Spits out various info in relatiuon to visible markers
    '''
    :param marker: sr.robot3 marker
    :return: [marker, ho, vo, distance]
    '''
    return [marker, marker.position.horizontal_angle, marker.position.vertical_angle, marker.position.distance]


def movement_calculate(target):
    # converts radians to degrees
    mov_angle = math.degrees(target.position.horizontal_angle)
    return [mov_angle, target.position.distance]


def distance_update(robot, target_id):
    # runs every iteration to update the distance and angle by target ID
    markers = robot.camera.see()
    for marker in markers:
        if marker.id == target_id:
            return marker.position.distance, marker.position.horizontal_angle

''' Please comment this it is almost unreadable'''
""" Disagree there ie enough comments"""
# no, make this clearer so other people can fix it if it breaks