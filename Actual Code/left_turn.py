from machine import Pin, PWM
from utime import sleep
import _thread
import sys
from class_definitions import Motor


def input_irq_19(p):
    "Interrupt handler"
    # print(p)
    value = p.value()
    print(f"Input changed, value={value}")

    if value == 1:

        motor3 = Motor(dirPin=4, PWMPin=5)  # Motor 3 is controlled from Motor Driv2 #1, which is on GP/5
        motor4 = Motor(dirPin=7, PWMPin=6)  # Motor 4 is controlled from Motor Driv2 #2, which is on GP6/7

        input_pin = 19  # Pin 19 = GP19 (labelled 25 on the jumper)
        input = Pin(input_pin, Pin.IN, Pin.PULL_DOWN) # Think carefully whether you need pull up or pull down
        motor3.Reverse(60)  # Motor 3 moves backward at 60% speed
        motor4.Forward(60)  # Motor 4 moves forward at 60% speed
        sleep(1.3)  # Run both motors for 1.3 seconds
        motor3.off()
        motor4.off()

    else:
        print("No action on falling edge")


def intleft():
    "More advanced, interrupt based input handling"
    input_pin = 19  # Pin 17 = GP17 (labelled 25 on the jumper)
    input = Pin(input_pin, Pin.IN, Pin.PULL_DOWN) # Think carefully whether you need pull up or pull down
    input.irq(handler=input_irq_19) # Register irq, you could also consider rising and falling edges c.f. https://docs.micropython.org/en/latest/library/machine.Pin.html

    while True:
        pass # irq handling does the rest in this instance

if __name__ == "__main__":
    intleft()
