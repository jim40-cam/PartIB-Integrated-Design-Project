from machine import Pin, I2C
from time import sleep
from libs.tiny_code_reader.tiny_code_reader import TinyCodeReader #type: ignore
from libs.VL53L0X.VL53L0X import VL53L0X #type: ignore


def read_qr_when_close(
    i2c_id=0,
    scl_pin=17,
    sda_pin=16,
    freq=400000,
    target_distance_mm=180,
    distance_tolerance=10,
    poll_delay=None
):
    """
    Wait until the robot is within ~target_distance_mm of an object, 
    then read and parse a QR code.

    Returns:
        dict or None: {'rack': 'A', 'level': 'U', 'position': 6}
                      or None if nothing detected.
    """

    # --- Initialize shared I2C bus ---
    i2c = I2C(i2c_id, scl=Pin(scl_pin), sda=Pin(sda_pin), freq=freq)

    # --- Distance sensor setup ---
    tof = VL53L0X(i2c)
    print("VL53L0X ready, measuring distance...")

    # --- Wait until close enough ---
    while True:
        distance = tof.read()  # distance in mm
        print(f"Distance: {distance} mm")

        if abs(distance - target_distance_mm) <= distance_tolerance:
            print(f"Within range ({target_distance_mm} ± {distance_tolerance} mm). Starting QR scan.")
            break

        sleep(0.05)

    # --- Tiny Code Reader setup ---
    devices = i2c.scan()
    if 0x0C not in devices:
        print("Tiny Code Reader not detected at 0x0C.")
        return None

    reader = TinyCodeReader(i2c)
    delay = poll_delay or TinyCodeReader.TINY_CODE_READER_DELAY

    print("Scanning for QR code...")

    # --- Poll until QR code found ---
    while True:
        code = reader.poll()
        if code:
            print(f"QR Code detected: {code}")
            parsed = parse_qr_code(code)
            print(f"Parsed code: {parsed}")
            return parsed
        sleep(delay)


def parse_qr_code(code_str):
    """
    Parse a QR code string like 'Rack A, Upper, 6' into a structured dict:
      {'rack': 'A', 'level': 'U', 'position': 6}
    """
    try:
        parts = [p.strip() for p in code_str.split(",")]
        rack = parts[0].replace("Rack", "").strip().upper()  # 'A' or 'B'
        level_word = parts[1].strip().capitalize()  # 'Upper' or 'Lower'
        level = 'U' if level_word == 'Upper' else 'L'
        position = int(parts[2])
        return {"rack": rack, "level": level, "position": position}
    except Exception as e:
        print(f"Error parsing QR code '{code_str}': {e}")
        return {"raw": code_str}

