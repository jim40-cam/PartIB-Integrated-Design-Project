from machine import Pin, PWM
from utime import sleep
import _thread
import sys
from class_definitions import Motor
from final_forward import forward_move
from final_right import intright
from final_left import intleft

def location_movement(location):
    motor3 = Motor(dirPin=4, PWMPin=5)  # Motor 3 is controlled from Motor Driv2 #1, which is on GP/5
    motor4 = Motor(dirPin=7, PWMPin=6)  # Motor 4 is controlled from Motor Driv2 #2, which is on GP6/7

    # Set both motors to move backward
    input9 = Pin(9, Pin.IN, Pin.PULL_DOWN) # 16 is for left
    input10 = Pin(10, Pin.IN, Pin.PULL_DOWN) # 17 is for right
    input11 = Pin(11, Pin.IN, Pin.PULL_DOWN) # 18 is for far left
    input12 = Pin(12, Pin.IN, Pin.PULL_DOWN) # 19 is for far right

    for loc in location:
        if loc == "f":
            forward()
        elif loc == "r":
            input_pin = 12 
            input = Pin(input_pin, Pin.IN, Pin.PULL_DOWN) # Think carefully whether you need pull up or pull down
            input.irq(handler=intright)
        elif loc == "l":
            input_pin = 11
            input = Pin(input_pin, Pin.IN, Pin.PULL_DOWN)  # Think carefully whether you need pull up or pull down
            input.irq(handler=intleft)
        else:
            motor3.off()
            motor4.off()
        sleep(0.1)  # Small delay between movements