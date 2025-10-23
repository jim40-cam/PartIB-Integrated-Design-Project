from machine import Pin, PWM
from utime import sleep
import _thread
import sys
from .forward_movement import Motor


def right():

    motor3 = Motor(dirPin=4, PWMPin=5)  # Motor 3 is controlled from Motor Driv2 #1, which is on GP/5
    motor4 = Motor(dirPin=7, PWMPin=6)  # Motor 4 is controlled from Motor Driv2 #2, which is on GP6/7

    # Set both motors to move backward
    motor3.Reverse(60)  # Motor 3 moves backward at 50% speed
    motor4.Reverse(60)  # Motor 4 moves backward at 50% speed

    # Keep the motors running for a specific duration
    sleep(1.3)  # Run both motors for 1.5 seconds

    # Turn off both motors
    motor3.off()
    motor4.off()


def input_irq_16(p):
    "Interrupt handler"
    # print(p)
    value = p.value()
    print(f"Input changed, value={value}")

    if value == 1:

        motor3 = Motor(dirPin=4, PWMPin=5)  # Motor 3 is controlled from Motor Driv2 #1, which is on GP/5
        motor4 = Motor(dirPin=7, PWMPin=6)  # Motor 4 is controlled from Motor Driv2 #2, which is on GP6/7

        # Set both motors to move backward
        motor3.Reverse(60)  # Motor 3 moves backward at 50% speed
        motor4.Reverse(60)  # Motor 4 moves backward at 50% speed

        # Keep the motors running for a specific duration
        sleep(1.3)  # Run both motors for 1.5 seconds

        # Turn off both motors
        motor3.off()
        motor4.off()

    else:
        print("No action on falling edge")


def start_input_irq_16():
    "More advanced, interrupt based input handling"
    input_pin = 16  # Pin 16 = GP16 (labelled 24 on the jumper)
    input = Pin(input_pin, Pin.IN, Pin.PULL_DOWN) # Think carefully whether you need pull up or pull down
    input.irq(handler=input_irq_16) # Register irq, you could also consider rising and falling edges c.f. https://docs.micropython.org/en/latest/library/machine.Pin.html

    while True:
        pass # irq handling does the rest in this instance

if __name__ == "__main__":
    start_input_irq_16()

start_input_irq_16()