from machine import Pin, I2C # type: ignore (will work on pico)
from time import sleep
# will this work on pico? possibly
from libs.tiny_code_reader.tiny_code_reader import TinyCodeReader #type: ignore
from libs.VL53L0X.VL53L0X import VL53L0X #type: ignore

def qr_to_vector(code_str):
    """
    Convert QR code string into numeric vector [rack_id, level_id, position].
        rack_id: 0 for Rack A, 1 for Rack B
        level_id: 0 for Lower, 1 for Upper
        position: int 1–6

    Args:
        code_str (str): QR code string in format "RACK_LEVEL_POSITION"

    Returns:
        list[int] or None: [rack_id, level_id, position] or None if invalid
    """
    try:
        parts = [p.strip() for p in code_str.split(',')]
        rack_str = parts[0].split()[-1].upper() # A or B
        level_str = parts[1].capitalize() # Upper or Lower
        pos = int(parts[2]) # 1-6

        rack = 0 if rack_str == 'A' else 1 if rack_str == 'B' else None
        level = 0 if level_str == 'Lower' else 1 if level_str == 'Upper' else None

        return[rack, level, pos] if None not in (rack, level) and 1 <= pos <= 6 else None
    except Exception as e:
        print(f"Error parsing QR code '{code_str}': {e}")
        return None

def scan_qr_code(i2c_id=0, scl_pin=17, sda_pin=16, freq=400000, target_distance_mm=180, distance_tolerance=10, poll_delay=None):
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

    # Wait until within target distance
    while True:
        distance = tof.read()
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

    delay = poll_delay or TinyCodeReader.TINY_CODE_READER_DELAY

    # Poll until a QR code is found
    while True:
        code = reader.poll()
        if code:
            print(f"QR Code detected: {code}")
            vector = qr_to_vector(code)
            print(f"QR vector: {vector}")
            return vector
        sleep(delay)

