from machine import Pin, PWM
from utime import sleep
import _thread
from class_definitions import Motor
from right_turn import intright
from left_turn import intleft
from forward_movement import forward

def tracking():
    motor3 = Motor(dirPin=4, PWMPin=5)  # Motor 3 is controlled from Motor Driv2 #1, which is on GP/5
    motor4 = Motor(dirPin=7, PWMPin=6)  # Motor 4 is controlled from Motor Driv2 #2, which is on GP6/7

    # Set both motors to move backward
    input16 = Pin(16, Pin.IN, Pin.PULL_DOWN) # 16 is for left
    input17 = Pin(17, Pin.IN, Pin.PULL_DOWN) # 17 is for right
    input18 = Pin(18, Pin.IN, Pin.PULL_DOWN) # 18 is for far left
    input19 = Pin(19, Pin.IN, Pin.PULL_DOWN) # 19 is for far right

    forward()

    while True:
        if input16.value() == 1 and input18.value() == 1:
            sleep(3)
            forward()
        elif input17.value() == 1 and input19.value() == 1:
            sleep(3)
            forward()
    