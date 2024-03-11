from sr.robot3 import *
import time
pi = 3.14159
robot = Robot()

def vision_update():
    markers = robot.camera.see()
    if markers:
        return markers[0]
    else:
        return False

def angle_led(marker):
    angle = marker.position.horizontal_angle * (180/pi)
    led_cont = robot.kch.leds
    led_cont[LED_A].colour = Colour.OFF
    led_cont[LED_B].colour = Colour.OFF
    led_cont[LED_C].colour = Colour.OFF
    if angle <= -15:
        led_cont[LED_A].colour = Colour.YELLOW
    elif angle >= 15:
        led_cont[LED_C].colour = Colour.YELLOW
    else:
        led_cont[LED_B].colour = Colour.YELLOW

while True:
    time.sleep(0.01)
    val = vision_update()
    if val:
        angle_led(val)