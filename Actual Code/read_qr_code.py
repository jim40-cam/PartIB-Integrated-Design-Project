# read qr code 

from machine import Pin, I2C  # type: ignore (will work on pico)
from time import sleep
# will this work on pico? possibly 
from libs.tiny_code_reader.tiny_code_reader import TinyCodeReader #type: ignore

# =============================
# Setup
# =============================

# I2C0 on GP16 (SDA) and GP17 (SCL)
# Change pins if you wired differently
i2c = I2C(0, scl=Pin(17), sda=Pin(16), freq=400000)

# Scan I2C bus to verify device is detected
devices = i2c.scan()
print("I2C devices found:", devices)

if 0x0C not in devices:
    print("Tiny Code Reader not detected! Check wiring and power.")
else:
    print("Tiny Code Reader detected at address 0x0C")

# Initialize the reader
reader = TinyCodeReader(i2c)
print("Tiny Code Reader ready — hold a QR code ~180 mm in front...")

# =============================
# Main loop
# =============================

while True:
    code = reader.poll()  # Try to read a QR code
    if code:
        print(f"QR Code detected: {code}")

        # Optional: small pause to avoid printing the same code repeatedly
        sleep(1)

    sleep(TinyCodeReader.TINY_CODE_READER_DELAY)
