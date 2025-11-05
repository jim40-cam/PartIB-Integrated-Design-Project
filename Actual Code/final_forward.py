from machine import Pin, PWM
from utime import sleep
import _thread
from class_definitions import Motor

def forward_move():
    motor3 = Motor(dirPin=4, PWMPin=5)  # Motor 3 is controlled from Motor Driv2 #1, which is on GP/5
    motor4 = Motor(dirPin=7, PWMPin=6)  # Motor 4 is controlled from Motor Driv2 #2, which is on GP6/7

    # Set both motors to move backward
    input9 = Pin(9, Pin.IN, Pin.PULL_DOWN) # 16 is for left
    input10 = Pin(10, Pin.IN, Pin.PULL_DOWN) # 17 is for right
    input11 = Pin(11, Pin.IN, Pin.PULL_DOWN) # 18 is for far left
    input12 = Pin(12, Pin.IN, Pin.PULL_DOWN) # 19 is for far right
    
    while True:
        print (f"Input9: {input9.value()}, Input10: {input10.value()}, Input11: {input11.value()}, Input12 {input12.value()}")
        if input9.value() == 0 and input10.value() == 0:
            motor3.Forward(50)  # Motor 3 moves backward at 60% speed
            motor4.Forward(50)  # Motor 4 moves forward at 50% speed
            
        elif input9.value() == 1 and input10.value() == 0:
            motor3.Forward(40)  # Motor 3 moves backward at 70% speed
            motor4.Forward(60)  # Motor 4 moves forward at 60% speed

        elif input9.value() == 0 and input10.value() == 1:
            motor3.Forward(60)  # Motor 3 moves backward at 60% speed
            motor4.Forward(40)  # Motor 4 moves forward at 70% speed
        
        elif input9.value() == 1 or input10.value() == 1:
            break
        if input11.value() == 1 or input12.value() == 1:
            break
        
        sleep(0.3)
        motor3.off()
        motor4.off()
            

