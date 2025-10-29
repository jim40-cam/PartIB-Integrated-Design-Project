from machine import Pin, PWM
from utime import sleep
import _thread
from class_definitions import Motor

def forward():
    motor3 = Motor(dirPin=4, PWMPin=5)  # Motor 3 is controlled from Motor Driv2 #1, which is on GP/5
    motor4 = Motor(dirPin=7, PWMPin=6)  # Motor 4 is controlled from Motor Driv2 #2, which is on GP6/7

    # Set both motors to move backward
    input6 = Pin(6, Pin.IN, Pin.PULL_DOWN) # 16 is for left
    input7 = Pin(7, Pin.IN, Pin.PULL_DOWN) # 17 is for right
    input9 = Pin(9, Pin.IN, Pin.PULL_DOWN) # 18 is for far left
    input10 = Pin(10, Pin.IN, Pin.PULL_DOWN) # 19 is for far right
    
    while True:
        print (f"Input6: {input6.value()}, Input7: {input7.value()}, Input9: {input9.value()}, Input10 {input10.value()}")
        if input6.value() == 0 and input7.value() == 0:
            motor3.Forward(60)  # Motor 3 moves backward at 60% speed
            motor4.Forward(60)  # Motor 4 moves forward at 50% speed
            
        elif input6.value() == 1 and input7.value() == 0:
            motor3.Forward(60)  # Motor 3 moves backward at 70% speed
            motor4.Forward(80)  # Motor 4 moves forward at 60% speed

        elif input6.value() == 0 and input7.value() == 1:
            motor3.Forward(80)  # Motor 3 moves backward at 60% speed
            motor4.Forward(60)  # Motor 4 moves forward at 70% speed
        
        elif input8.value() == 1 or input9.value() == 1:
            motor3.off()
            motor4.off()
            
        sleep(0.1)  # Small delay to avoid overwhelming the CPU

forward()


