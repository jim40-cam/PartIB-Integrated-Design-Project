from machine import Pin, PWM
from utime import sleep
import _thread
from class_definitions import Motor
from right_turn import intright
from left_turn import intleft

def forward():
    motor3 = Motor(dirPin=4, PWMPin=5)  # Motor 3 is controlled from Motor Driv2 #1, which is on GP/5
    motor4 = Motor(dirPin=7, PWMPin=6)  # Motor 4 is controlled from Motor Driv2 #2, which is on GP6/7

    # Set both motors to move backward
    input16 = Pin(16, Pin.IN, Pin.PULL_DOWN) # 16 is for left
    input17 = Pin(17, Pin.IN, Pin.PULL_DOWN) # 17 is for right
    input18 = Pin(18, Pin.IN, Pin.PULL_DOWN) # 18 is for far left
    input19 = Pin(19, Pin.IN, Pin.PULL_DOWN) # 19 is for far right
    
    while True:
        print (f"Input16: {input16.value()}, Input17: {input17.value()}, Input18: {input18.value()}, Input19: {input19.value()}")
        if input16.value() == 0 and input17.value() == 0:
            motor3.Forward(60)  # Motor 3 moves backward at 60% speed
            motor4.Forward(60)  # Motor 4 moves forward at 50% speed
            
        elif input16.value() == 1 and input17.value() == 0:
            motor3.Forward(60)  # Motor 3 moves backward at 70% speed
            motor4.Forward(80)  # Motor 4 moves forward at 60% speed

        elif input16.value() == 0 and input17.value() == 1:
            motor3.Forward(80)  # Motor 3 moves backward at 60% speed
            motor4.Forward(60)  # Motor 4 moves forward at 70% speed
            
        elif input16.value() == 1 and input18.value() == 1:
            input_pin = 18
            input = Pin(input_pin, Pin.IN, Pin.PULL_DOWN)  # Think carefully whether you need pull up or pull down
            input.irq(handler=intleft)
            sleep(3)  
            
        elif input17.value() == 1 and input19.value() == 1:
            input_pin = 19 
            input = Pin(input_pin, Pin.IN, Pin.PULL_DOWN) # Think carefully whether you need pull up or pull down
            input.irq(handler=intright) 
            sleep(3)
        elif input16.value() == 1 and input17.value() == 1:
            motor3.off()
            motor4.off()
        sleep(0.1)  # Small delay to avoid overwhelming the CPU
        
forward()



