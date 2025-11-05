#only contains the functions imported from the other modules
#functions will only be run in here
from right_turn import intright
from left_turn import intleft
from track_current_location import tracking
from forward_movement import forward
from machine import Pin, PWM
from utime import sleep
from final_location_reader import location_movement

button_pin = 26
button = Pin(button_pin, Pin.IN, Pin.PULL_DOWN)
while True:
    if button.value() == 0:
        sleep(0.1)
        pass
    else:
        break
location = "fflff"
location_movement(location)