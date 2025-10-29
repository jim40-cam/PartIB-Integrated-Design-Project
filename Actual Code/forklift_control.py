# forklift_control.py
from machine import Pin, PWM, I2C #type: ignore (will work on pico)
import time
from libs.VL53L0X.VL53L0X import VL53L0X #type: ignore
from time import sleep
from .forward_movement import Motor

# LINEAR ACTUATOR SETUP
ENA_PIN = 5
IN1_PIN = 4
IN2_PIN = 3

ena = Pin(ENA_PIN, Pin.OUT)
in1 = Pin(IN1_PIN, Pin.OUT)
in2 = Pin(IN2_PIN, Pin.OUT)
ena.value(1)  # Enable motor driver

# LINEAR ACTUATOR CONTROL

def lift_up(duration_s=3.0): #edit time to change lift height
    """Extend actuator to lift forklift up."""
    print("Lifting up...")
    in1.value(1)
    in2.value(0)
    time.sleep(duration_s)
    stop_actuator()
    print("Lift up complete.")

def lift_down(duration_s=3.0): #edit time to change lift height
    """Retract actuator to lower forklift."""
    print("Lowering down...")
    in1.value(0)
    in2.value(1)
    time.sleep(duration_s)
    stop_actuator()
    print("Lift down complete.")

def stop_actuator():
    """Stop actuator motion."""
    in1.value(0)
    in2.value(0)

# FORKLIFT FUNCTION 

def pick_up_box(
    i2c_id=0,
    scl_pin=17,
    sda_pin=16,
    freq=400000,
    approach_distance=20,   # distance in mm at which to start pickup
    box_present_threshold=40,  # consider "box detected" if <40mm away
    lift_down_time=2.0,
    lift_up_time=2.0
):
    """
    1. Wait until the box is within `approach_distance` mm.
    2. Lower forks.
    3. Move robot forward to slide under box.
    4. Lift forks.
    5. Confirm box presence using VL53L0X.
    """
    # Setup I2C and distance sensor
    i2c = I2C(i2c_id, scl=Pin(scl_pin), sda=Pin(sda_pin), freq=freq)
    tof = VL53L0X(i2c)
    print("VL53L0X sensor ready.")

    # Wait until close enough to box
    # Do i need to add a while moving forward here????
    print("Approaching box...")
    while True:
        distance = tof.read() - 40  # subtract your 40mm offset
        print(f"Distance: {distance} mm")
        if distance <= approach_distance:
            print("Box within pickup range.")
            break
        sleep(0.05)

    # Lower forks
    print("Lowering forks...")
    lift_down(lift_down_time)

    # --- Move robot forward slightly ---
    print("Moving forward to engage box...")

    motor3 = Motor(dirPin=4, PWMPin=5)
    motor4 = Motor(dirPin=7, PWMPin=6)

    motor3.Forward(50)
    motor4.Forward(50)
    sleep(1.0)   # move forward for 1 second — adjust for your setup
    motor3.off()
    motor4.off()
    print("Robot positioned under box.")

    # Lift box
    print("Lifting box...")
    lift_up(lift_up_time)

    # Confirm pickup 
    sleep(0.5)  # small pause before measuring again
    distance_after = tof.read() - 40
    print(f"Distance after lift: {distance_after} mm")

    if distance_after <= box_present_threshold:
        print("Success")
        return True
    else:
        print("Oops")
        return False