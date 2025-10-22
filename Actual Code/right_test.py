from machine import Pin, PWM
from utime import sleep
import _thread
import sys
sys.path.append("c:/Users/super/OneDrive - University of Cambridge/2025-2026 Cam/IEP V2/PartIB-Integrated-Design-Project-1/Actual Code")
from forward_movement import forward

class Motor:
    def __init__(self, dirPin, PWMPin):
        self.mDir = Pin(dirPin, Pin.OUT)  # set motor direction pin
        self.pwm = PWM(Pin(PWMPin))  # set motor pwm pin
        self.pwm.freq(1000)  # set PWM frequency
        self.pwm.duty_u16(0)  # set duty cycle - 0=off
        
    def off(self):
        self.pwm.duty_u16(0)
        
    def Forward(self, speed=100):
        self.mDir.value(0)                     # forward = 0 reverse = 1 motor
        self.pwm.duty_u16(int(65535 * speed / 100))  # speed range 0-100 motor

    def Reverse(self, speed=30):
        self.mDir.value(1)
        self.pwm.duty_u16(int(65535 * speed / 100))


def input_irq_16(p):
    "Interrupt handler"
    # print(p)
    value = p.value()
    print(f"Input changed, value={value}")

    if value == 1:

        motor3 = Motor(dirPin=4, PWMPin=5)  # Motor 3 is controlled from Motor Driv2 #1, which is on GP/5
        motor4 = Motor(dirPin=7, PWMPin=6)  # Motor 4 is controlled from Motor Driv2 #2, which is on GP6/7

        input_pin = 19  # Pin 19 = GP19 (labelled 25 on the jumper)
        input = Pin(input_pin, Pin.IN, Pin.PULL_DOWN) # Think carefully whether you need pull up or pull down
        motor3.Forward(60)  # Motor 3 moves backward at 60% speed
        motor4.Reverse(60)  # Motor 4 moves forward at 60% speed
        sleep(1.3)  # Run both motors for 1.3 seconds
        motor3.off()
        motor4.off()

    else:
        print("No action on falling edge")


def start_input_irq_16():
    "More advanced, interrupt based input handling"
    input_pin = 19  # Pin 17 = GP17 (labelled 25 on the jumper)
    input = Pin(input_pin, Pin.IN, Pin.PULL_DOWN) # Think carefully whether you need pull up or pull down
    input.irq(handler=input_irq_16) # Register irq, you could also consider rising and falling edges c.f. https://docs.micropython.org/en/latest/library/machine.Pin.html

    while True:
        pass # irq handling does the rest in this instance

if __name__ == "__main__":
    start_input_irq_16()
