from machine import Pin, PWM
from utime import sleep
import _thread
import sys
from class_definitions import Motor

def location_movement(location):
    motor3 = Motor(dirPin=4, PWMPin=5)  # Motor 3 is controlled from Motor Driv2 #1, which is on GP/5
    motor4 = Motor(dirPin=7, PWMPin=6)  # Motor 4 is controlled from Motor Driv2 #2, which is on GP6/7

    # Set both motors to move backward
    input16 = Pin(6, Pin.IN, Pin.PULL_DOWN) # 16 is for left
    input17 = Pin(7, Pin.IN, Pin.PULL_DOWN) # 17 is for right
    input18 = Pin(9, Pin.IN, Pin.PULL_DOWN) # 18 is for far left
    input19 = Pin(10, Pin.IN, Pin.PULL_DOWN) # 19 is for far right

    for loc in location:
        if loc == "f":
            print("f")
            motor3.Forward(60)  # Motor 3 moves backward at 60% speed
            motor4.Forward(60)  # Motor 4 moves forward at 50% speed
            sleep(1)
        elif loc == "r":
            print("r")
            motor3.Forward(60)  # Motor 3 moves backward at 60% speed
            motor4.Reverse(60)  # Motor 4 moves forward at 50% speed
            sleep(1)
        elif loc == "l":
            print("l")
            motor3.Reverse(60)  # Motor 3 moves backward at 60% speed
            motor4.Forward(60)  # Motor 4 moves forward at 50% speed
            sleep(1)
        sleep(0.1)  # Small delay between movements

location = "ffrfflff"
location_movement(location)
motor3 = Motor(dirPin=4, PWMPin=5)  # Motor 3 is controlled from Motor Driv2 #1, which is on GP/5
motor4 = Motor(dirPin=7, PWMPin=6)  # Motor 4 is controlled from Motor Driv2 #2, which is on GP6/7
motor3.off()
motor4.off()