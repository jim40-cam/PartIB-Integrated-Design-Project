from machine import Pin, PWM
from utime import sleep
import _thread

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



def forward():
    motor3 = Motor(dirPin=4, PWMPin=5)  # Motor 3 is controlled from Motor Driv2 #1, which is on GP/5
    motor4 = Motor(dirPin=7, PWMPin=6)  # Motor 4 is controlled from Motor Driv2 #2, which is on GP6/7

    # Set both motors to move backward
    input16 = Pin(16, Pin.IN, Pin.PULL_DOWN) # 16 is for left
    input17 = Pin(17, Pin.IN, Pin.PULL_DOWN) # 17 is for right
    input18 = Pin(18, Pin.IN, Pin.PULL_DOWN) # 18 is for far left
    input19 = Pin(19, Pin.IN, Pin.PULL_DOWN) # 19 is for far right

    while True:
        print (f"Input16: {input16.value()}, Input17: {input17.value()}")
        if input16.value() == 0 and input17.value() == 0:
            motor3.Forward(60)  # Motor 3 moves backward at 60% speed
            motor4.Forward(60)  # Motor 4 moves forward at 50% speed

        elif input16.value() == 1 and input17.value() == 0:
            motor3.Forward(60)  # Motor 3 moves backward at 70% speed
            motor4.Forward(70)  # Motor 4 moves forward at 60% speed

        elif input16.value() == 0 and input17.value() == 1:
            motor3.Forward(70)  # Motor 3 moves backward at 60% speed
            motor4.Forward(60)  # Motor 4 moves forward at 70% speed
        else:
            break
    # Turn off both motors
    motor3.off()
    motor4.off()

if __name__ == "__main__":
    forward()
