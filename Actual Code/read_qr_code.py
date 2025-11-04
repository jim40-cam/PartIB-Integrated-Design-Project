from class_definitions import Motor
from machine import Pin, I2C # type: ignore (will work on pico)
from time import sleep
# will this work on pico? possibly
from libs.tiny_code_reader.tiny_code_reader import TinyCodeReader #type: ignore
from libs.VL53L0X.VL53L0X import VL53L0X #type: ignore

def parse_qr(code_str):
    """
    Convert QR code string into list [rack, level, position].
        rack: 'A' or 'B'
        level: 'L' for Lower, 'U' for Upper
        position: int 1–6

    Args:
        code_str (str): QR code string in format like "Rack A, Lower, 6"

    Returns:
        list or None: ['A', 'L', 6] or ['B', 'U', 3], or None if invalid
    """
    try:
        parts = [p.strip() for p in code_str.split(',')]
        rack_str = parts[0].split()[-1].upper()   # A or B
        level_str = parts[1].capitalize()         # Upper or Lower
        pos = int(parts[2])                       # 1–6

        # Convert to compact form
        level_short = 'L' if level_str == 'Lower' else 'U' if level_str == 'Upper' else None

        if rack_str in ('A', 'B') and level_short in ('L', 'U') and 1 <= pos <= 6:
            parsed = [rack_str, level_short, pos]
            return parsed
        else:
            print(f"Invalid QR code format: {code_str}")
            return None

    except Exception as e:
        print(f"Error parsing QR code '{code_str}': {e}")
        return None


def scan_qr_code(i2c_id=0, scl_pin=17, sda_pin=16, freq=400000, target_distance_mm=200, distance_tolerance=10, poll_delay=None):
    """
     Wait until robot is ~target_distance_mm away, then read a QR code and 
    convert it into a numeric vector [rack_id, level_id, position].
        rack_id: 0 for Rack A, 1 for Rack B
        level_id: 0 for Lower, 1 for Upper
        position: int 1–6
    
    Args:
        i2c_id (int): I2C bus ID (default 0)
        scl_pin (int): GPIO pin for SCL
        sda_pin (int): GPIO pin for SDA
        freq (int): I2C frequency in Hz
        poll_delay (float): optional delay override between polls

    Returns:
        list[int] or None


    """

    # Initialize I2C
    i2c = I2C(i2c_id, scl=Pin(scl_pin), sda=Pin(sda_pin), freq=freq)

    # Initialize distance sensor
    tof = VL53L0X(i2c)
    print("Distance sensor initialised.")
    
    # set up LED
    scan_led = Pin(22, Pin.OUT)  # GP22 indicator LED
    scan_led.value(0)            # start OFF

    # move it forward about 5cm from start junction, add code here

    motor3 = Motor(dirPin=4, PWMPin=5)  # Motor 3 is controlled from Motor Driv2 #1, which is on GP/5
    motor4 = Motor(dirPin=7, PWMPin=6)  # Motor 4 is controlled from Motor Driv2 #2, which is on GP6/7
    motor3.off()
    motor4.off()
    motor3.Forward(60)
    motor4.Forward(60)
    sleep(0.8)

    # Wait until within target distance, may need to experiment to find what this is 
    # do we still need this ?????
    while True:
        distance = tof.read() - 40 # adjust for sensor offset
        print(f"Distance: {distance} mm")
        if abs(distance - target_distance_mm) <= distance_tolerance:
            print("Within target distance.")
            break
        sleep(0.05)  # small delay to avoid busy-waiting

    devices = i2c.scan()
    if 0x0C not in devices:
        print("Tiny Code Reader not detected at address 0x0C.")
        return None
    

    reader = TinyCodeReader(i2c)
    print("Tiny Code Reader ready — scanning for QR codes...")

    scan_led.value(1)

    delay = poll_delay or TinyCodeReader.TINY_CODE_READER_DELAY

    # Poll until a QR code is found
    try:
        while True:
            code = reader.poll()
            if code:
                print(f"QR Code detected: {code}")
                parsed = parse_qr(code)
                print(f"QR parsed: {parsed}")
                if parsed:
                    return tuple(parsed)
            sleep(delay)
    finally:
        # turn off LED
        scan_led.value(0)
