import sr.robot3
import cv2 as cv
import math

'''
Assumptions I am making:

- Different processes/thread
- Robot goes for closest marker (asteroid) first
'''
# ini

def vision_run(robot, save=False, dev=False, ):
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
        return move_values

def marker_sort(current_markers):
    # sort markers by distance,
    sorted_markers = []
    for marker in current_markers:
        position = markerpos(marker)
        sorted_markers.append(position)
    sorted(sorted_markers, key=lambda x: x[3])  # element at index 3 is distance
    target_marker = current_markers[current_markers.index(sorted_markers[0][0])]
    return target_marker


def markerpos(marker):
    '''
    :param marker: sr.robot3 marker
    :return: [ho, vo, distance]
    '''
    return [marker, marker.position.horizontal_angle, marker.position.vertical_angle, marker.position.distance]


def movement_calculate(target):
    mov_angle = math.degrees(target.position.horizontal_angle)
    return [mov_angle, target.position.distance]

