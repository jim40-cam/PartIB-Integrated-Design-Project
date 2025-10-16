# forklift_control.py
from machine import Pin, PWM #type: ignore (will work on pico)
import time

# ==============================
# LINEAR ACTUATOR SETUP
# ==============================
ENA_PIN = 5
IN1_PIN = 4
IN2_PIN = 3

ena = Pin(ENA_PIN, Pin.OUT)
in1 = Pin(IN1_PIN, Pin.OUT)
in2 = Pin(IN2_PIN, Pin.OUT)
ena.value(1)  # Enable motor driver

# ==============================
# SERVO SETUP (DSS-M15S)
# ==============================
# Main control on GP13
SERVO_PIN = 13
servo = PWM(Pin(SERVO_PIN))
servo.freq(50)  # Standard 50 Hz servo signal

# Helper: convert angle (0–270°) → duty cycle for 1–2 ms pulse width
def _servo_angle_to_duty(angle):
    min_duty = 1638   # corresponds to 1.0 ms at 50 Hz
    max_duty = 8192   # corresponds to 2.0 ms at 50 Hz
    duty = int(min_duty + (angle / 270) * (max_duty - min_duty))
    return max(min(duty, max_duty), min_duty)

# ==============================
# LINEAR ACTUATOR CONTROL
# ==============================
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

# ==============================
# SERVO CONTROL
# ==============================
def rotate_fork(angle):
    """Rotate servo to a given angle (0–270°)."""
    angle = max(0, min(angle, 270))
    duty = _servo_angle_to_duty(angle)
    servo.duty_u16(duty)
    print(f"Rotating fork to {angle}° (duty={duty})")

# ==============================
# EXAMPLE TEST
# ==============================
if __name__ == "__main__":
    print("Testing forklift control...")

    # Example: Lift up 23 mm (tune duration as needed)
    lift_up(duration_s=2.0)
    time.sleep(2)

    # Example: Rotate fork slightly
    rotate_fork(45)
    time.sleep(2)

    # Lower back down
    lift_down(duration_s=2.0)
