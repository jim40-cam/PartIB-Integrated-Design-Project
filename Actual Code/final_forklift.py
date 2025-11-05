# forklift_control.py
from machine import Pin, PWM, I2C # type: ignore (will work on pico)
from time import sleep
from libs.VL53L0X.VL53L0X import VL53L0X #type: ignore
from final_forward import Motor, forward
# from final_right import ? ask haruto 

def turn_around(turn_time=5, speed3=60, speed4=60): # check speeds, slightly different for each motor
    """
    Spin robot 180 degrees in place.
    Adjust turn_time for your specific robot’s rotation speed.
    """
    print("Turning around 180°...")
    motor3 = Motor(dirPin=4, PWMPin=5)
    motor4 = Motor(dirPin=7, PWMPin=6)

    # One motor forward, one motor reverse for spin
    motor3.Forward(speed3)
    motor4.Reverse(speed4)

    sleep(turn_time)
    motor3.off()
    motor4.off()
    print("Turn complete.")

# --- LINEAR ACTUATOR CLASS ---
class Actuator:
    def __init__(self, dirPin, PWMPin, freq=1000):
        """Initialize actuator motor driver."""
        self.mDir = Pin(dirPin, Pin.OUT)
        self.pwm = PWM(Pin(PWMPin))
        self.pwm.freq(freq)
        self.pwm.duty_u16(0)  # start stopped

    def set(self, direction: int, speed: int):
        """Set direction (0=extend, 1=retract) and speed (0–100%)."""
        self.mDir.value(direction)
        self.pwm.duty_u16(int(65535 * speed / 100))

    def stop(self):
        """Stop actuator."""
        self.pwm.duty_u16(0)


# --- INITIALISE ACTUATOR ---
actuator = Actuator(dirPin=0, PWMPin=1)  # adjust pins if needed


# --- ACTUATOR MOTION HELPERS ---
def lift_up(duration_s=3.0, speed=10):
    """Extend actuator to lift forklift up."""
    print(f"Lifting up for {duration_s}s at {speed}% speed...")
    actuator.set(direction=1, speed=speed)  # retract (up)
    sleep(duration_s)
    actuator.stop()
    print("Lift up complete.")


def lift_down(duration_s=3.0, speed=10): # edit speeds when testing
    """Retract actuator to lower forklift."""
    print(f"Lowering down for {duration_s}s at {speed}% speed...")
    actuator.set(direction=0, speed=speed)  # extend (down)
    sleep(duration_s)
    actuator.stop()
    print("Lift down complete.")


# FORKLIFT FUNCTION 
def pick_up_box(
    i2c_id=0,
    scl_pin=17,
    sda_pin=16,
    freq=400000,
    approach_distance=20,      # distance (mm) at which to start pickup
    box_present_threshold=40,  # consider "box detected" if <40 mm away
    lift_down_time=19.0,
    lift_up_time=19.0
):
    """
    0. Move forward
    1. Wait until the box is within `approach_distance` mm.
    2. Lower forks.
    3. Move robot forward to slide under box.
    4. Lift forks.
    5. Confirm box presence using VL53L0X.
    6. Turn around 180°.
    7. Call forward() to move it forward to next junction
    """
    # --- Setup distance sensor ---
    i2c = I2C(i2c_id, scl=Pin(scl_pin), sda=Pin(sda_pin), freq=freq)
    #tof = VL53L0X(i2c)
    print("VL53L0X sensor ready.")

    forward()

    # motor3 = Motor(dirPin=4, PWMPin=5)  # Motor 3 is controlled from Motor Driv2 #1, which is on GP/5
    # motor4 = Motor(dirPin=7, PWMPin=6)  # Motor 4 is controlled from Motor Driv2 #2, which is on GP6/7
    
    # motor3.Forward(60)
    # motor4.Forward(60)
    # sleep(0.8)
    # motor3.off()
    # motor4.off()



    # --- Wait until close enough to box ---
    # does this check need to be done???
    # while True:
    #     distance = tof.read() - 40  # apply offset
    #     print(f"Distance: {distance} mm")
    #     if distance <= approach_distance:
    #         print("Box within pickup range.")
    #         break
    #     sleep(0.05)

    # --- Lower forks ---
    lift_down(duration_s=lift_down_time, speed=25)

    # --- Move robot forward slightly ---
    print("Moving forward to engage box...")
    motor3 = Motor(dirPin=4, PWMPin=5)
    motor4 = Motor(dirPin=7, PWMPin=6)
    motor3.Forward(50)
    motor4.Forward(50)
    sleep(1.0)
    motor3.off()
    motor4.off()
    print("Robot positioned under box.")

    # --- Lift box ---
    lift_up(duration_s=lift_up_time, speed=25)
    sleep(1.0)  # small pause before moving forward again

    # # --- Confirm pickup ---
    # sleep(0.5)
    # distance_after = tof.read() - 40
    # print(f"Distance after lift: {distance_after} mm")

    # if distance_after <= box_present_threshold:
    #     print("Box successfully picked up!")
    # else:
    #     print("Box pickup failed.")
    #     return False
    

    # Turn around 180*, 
    turn_around(turn_time=5, speed3=60, speed4=60)  # adjust time and speeds as needed

    # Call forward() to move it forward to next junction
    forward() 
    return True


def put_down_box(
    parsed,
    i2c_id=0,
    scl_pin=17,
    sda_pin=16,
    freq=400000,
    move_forward_time=1.0,   # how long to move forward to position box
    lift_down_time=19.0,     # duration for full lowering
    partial_down_time=2.0,   # duration for partial lowering
    move_back_time=1.0       # how long to reverse after placing box
    # Need to test to confirm all of these times
):
    """
    Place a box based on whether it belongs to the Upper or Lower rack.

    Args:
        parsed: tuple like ('A', 'U', 3) from parse_qr()
    """

    # --- Setup motors and distance sensor ---
    i2c = I2C(i2c_id, scl=Pin(scl_pin), sda=Pin(sda_pin), freq=freq)
    #tof = VL53L0X(i2c)
    #print("VL53L0X sensor ready.")

    motor3 = Motor(dirPin=4, PWMPin=5)
    motor4 = Motor(dirPin=7, PWMPin=6)

    # --- Common: Move forward to placement area ---
    print("Moving forward to place box...")
    motor3.Forward(50)
    motor4.Forward(50)
    sleep(move_forward_time)
    motor3.off()
    motor4.off()

    # --- Upper bay sequence ---
    if parsed[1] == 'U':
        print("Upper bay detected — placing box at upper level...")
        lift_down(duration_s=lift_down_time, speed=25)

    # --- Lower bay sequence ---
    elif parsed[1] == 'L':
        print("Lower bay detected — performing two-step lowering sequence...")
        # Step 1: lower slightly
        print("Lowering partially...")
        lift_down(duration_s=partial_down_time, speed=25)

        # Step 2: move back slightly to position
        print("Reversing to position for full lowering...")
        motor3.Reverse(50)
        motor4.Reverse(50)
        sleep(move_back_time)
        motor3.off()
        motor4.off()

        # Step 3: lower fully
        print("Lowering fully to release box...")
        lift_down(duration_s=lift_down_time - partial_down_time, speed=10)

    else:
        print(f"Unknown level in parsed data: {parsed[1]}")
        return False

    # --- Common: Move backward to clear the box ---
    print("Reversing to clear box...")
    motor3.Reverse(50)
    motor4.Reverse(50)
    sleep(move_back_time)
    motor3.off()
    motor4.off()



