from machine import Pin, SoftI2C, I2C
from libs.mfrc522_python.src.mfrc522 import BasicMFRC522
from utime import sleep

def test_mfrc522():
    # Both options works
    # i2c_bus = SoftI2C(sda=Pin(8), scl=Pin(9))  # I2C0 on GP8 & GP9
    i2c_bus = I2C(id=0, sda=Pin(8), scl=Pin(9), freq=1000000) # I2C0 on GP8 & GP9
    print(i2c_bus.scan())  # Get the address (nb 41=0x29)
    
    reader = BasicMFRC522(i2c_bus)

    while True:
        id = reader.read_id_no_block()
        if id:
            print(f"Found ID: {id}")
            for i in [3, 7, 11, 15]:
                try:
                    id, text = reader.read_no_block(i)
                    print(f">Sector {i}: id={id}, text={text}")                
                except Exception as e:
                    print(f"Error reading sector {i}:", e)
        else:
            print("Not detected...")
        sleep(0.5)


if __name__ == "__main__":
    test_mfrc522()
