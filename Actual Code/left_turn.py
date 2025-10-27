from machine import Pin, PWM
from utime import sleep
import _thread
import sys
from class_definitions import Motor


def intleft(p):
    "Interrupt handler"
    # print(p)
    value = p.value()
    print(f"Input changed, value={value}")

    motor3 = Motor(dirPin=4, PWMPin=5)  # Motor 3 is controlled from Motor Driv2 #1, which is on GP/5
    motor4 = Motor(dirPin=7, PWMPin=6)  # Motor 4 is controlled from Motor Driv2 #2, which is on GP6/7
    motor3.Forward(60)
    motor4.Forward(60)
    sleep(0.8)
    
    motor3.Reverse(60)  # Motor 3 moves backward at 60% speed
    motor4.Forward(60)  # Motor 4 moves forward at 60% speed
    sleep(1.3)  # Run both motors for 1.3 seconds
    motor3.off()
    motor4.off()

if __name__ == "__main__":
    intleft()