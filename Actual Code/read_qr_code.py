from machine import Pin, I2C # type: ignore (will work on pico)
from time import sleep
# will this work on pico? possibly
from libs.tiny_code_reader.tiny_code_reader import TinyCodeReader #type: ignore


def scan_qr_code(i2c_id=0, scl_pin=17, sda_pin=16, freq=400000, poll_delay=None):
    """
    Reads a QR code using the Tiny Code Reader module over I2C.
    
    Args:
        i2c_id (int): I2C bus ID (default 0)
        scl_pin (int): GPIO pin for SCL
        sda_pin (int): GPIO pin for SDA
        freq (int): I2C frequency in Hz
        poll_delay (float): optional delay override between polls

    Returns:
        str or None: The decoded QR code string if found, otherwise None
    """

    # Initialize I2C
    i2c = I2C(i2c_id, scl=Pin(scl_pin), sda=Pin(sda_pin), freq=freq)

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
            return code  # return immediately once found
        sleep(delay)

