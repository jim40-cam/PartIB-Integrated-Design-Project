from machine import Pin, PWM
from utime import sleep
import _thread 

input16 = Pin(16, Pin.IN, Pin.PULL_DOWN) # 16 is for left
input17 = Pin(17, Pin.IN, Pin.PULL_DOWN) # 17 is for right
input18 = Pin(18, Pin.IN, Pin.PULL_DOWN) # 18 is for far left
input19 = Pin(19, Pin.IN, Pin.PULL_DOWN) # 19 is for far right
while True:
    print (f"Input16: {input16.value()}, Input17: {input17.value()}, Input18: {input18.value()}, Input19: {input19.value()}")
    sleep(0.1)