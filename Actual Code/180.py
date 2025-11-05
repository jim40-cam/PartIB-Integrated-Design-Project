from machine import Pin, PWM
from utime import sleep
import _thread
import sys
from class_definitions import Motor


def int180():
    motor3 = Motor(dirPin=4, PWMPin=5)  # Motor 3 is controlled from Motor Driv2 #1, which is on GP/5
    motor4 = Motor(dirPin=7, PWMPin=6)  # Motor 4 is controlled from Motor Driv2 #2, which is on GP6/7

    input9 = Pin(9, Pin.IN, Pin.PULL_DOWN) # 16 is for left
    input10 = Pin(10, Pin.IN, Pin.PULL_DOWN) # 17 is for right
    input11 = Pin(11, Pin.IN, Pin.PULL_DOWN) # 18 is for far left
    input12 = Pin(12, Pin.IN, Pin.PULL_DOWN) # 19 is for far right

    motor3.off()
    motor4.off()
    
    motor3.Forward(60)  # Motor 3 moves backward at 60% speed
    motor4.Reverse(60)  # Motor 4 moves forward at 60% speed
    sleep(3)
    input_pin = 9
    while True:
        if input9.value() == 0:
            sleep(0.1)
            pass
        else:
            break
    motor3.off()
    motor4.off()

def stopright(p):
    value = p.value()
    motor3 = Motor(dirPin=4, PWMPin=5)  # Motor 3 is controlled from Motor Driv2 #1, which is on GP/5
    motor4 = Motor(dirPin=7, PWMPin=6)  # Motor 4 is controlled from Motor Driv2 #2, which is on GP6/7
    print( f"Stopping right turn, value={value}")
    if value == 1:
        motor3.off()
        motor4.off()


