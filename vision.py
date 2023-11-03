import sr.robot3
import cv2 as cv

'''
Assumptions I am making:

- Different processes/thread
- Robot goes for closest marker (asterioid) first
'''
# ini
robot = sr.robot3.Robot()

current_markers = []


def cv2marker(save=False, dev=False):
    if not dev:
        # cv2 will allow us to adjust image info and make manipulations such as contrast if needed
        frame = robot.camera.capture()
        # run frame checks and manipulations etc
        markers = robot.camera.see(frame)
    else:  # capture doesnt work in simulation
        markers = robot.camera.see()
    if markers:
        current_markers = markers
        target_marker = marker_sort(current_markers)
        movement_calculate(target_marker)
    if not markers:
        current_markers.clear()


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
    '''
    For this section, I need to use the simulator to figure out a method
    of converting relative positions of the marker into instructions for
    controlling the movement, assumably this would be first centering the
    marker in the frame by turning so the centre of the marker is at the same
    pos as the centre of the camera, then moving to a fixed distance from the marker,
    from where it can pick up the marker.

    However, in DOCS, pixel coords needs to be used with the physical robot kit so we need
    to set up the webcam and print out a marker
    '''


if __name__ == "__main__":
    '''
    Values are set for testing, this script is not designed to be ran as a stand-alone
    script and instead as a module for other scripts to call upon
    however for simulating in we bots you will have to remove this condition
    as robot.py is called upon by another function
    '''
    while True:
        cv2marker(False, True)
