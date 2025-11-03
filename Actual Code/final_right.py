from machine import Pin, PWM
from utime import sleep
import _thread
import sys
from class_definitions import Motor


def intright(p):
    value = p.value()
    print(f"Input changed, value={value}")
    motor3 = Motor(dirPin=4, PWMPin=5)  # Motor 3 is controlled from Motor Driv2 #1, which is on GP/5
    motor4 = Motor(dirPin=7, PWMPin=6)  # Motor 4 is controlled from Motor Driv2 #2, which is on GP6/7

    input6 = Pin(6, Pin.IN, Pin.PULL_DOWN) # 16 is for left
    input7 = Pin(7, Pin.IN, Pin.PULL_DOWN) # 17 is for right
    input9 = Pin(9, Pin.IN, Pin.PULL_DOWN) # 18 is for far left
    input10 = Pin(10, Pin.IN, Pin.PULL_DOWN) # 19 is for far right

    motor3.off()
    motor4.off()

    motor3.Forward(60)
    motor4.Forward(60)
    sleep(0.8)
    
    motor3.Forward(60)  # Motor 3 moves backward at 60% speed
    motor4.Reverse(60)  # Motor 4 moves forward at 60% speed
    
    input_pin = 7
    input = Pin(input_pin, Pin.IN, Pin.PULL_DOWN)  # Think carefully whether you need pull up or pull down
    input.irq(handler=stopright)

    motor3.off()
    motor4.off()

def stopright(p):
    value = p.value()
    motor3 = Motor(dirPin=4, PWMPin=5)  # Motor 3 is controlled from Motor Driv2 #1, which is on GP/5
    motor4 = Motor(dirPin=7, PWMPin=6)  # Motor 4 is controlled from Motor Driv2 #2, which is on GP6/7
    if value == 0:
        motor3.off()
        motor4.off()

