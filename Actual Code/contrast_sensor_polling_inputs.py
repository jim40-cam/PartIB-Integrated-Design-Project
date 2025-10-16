from utime import sleep
from machine import Pin

def test_input_poll(input_pins):
    "Simple poll of input"
    while True:
        sleep(0.1)  # Small delay to avoid busy looping
        for pin in input_pins:
            input = Pin(pin, Pin.IN, Pin.PULL_DOWN) # Think carefully whether you need pull up or pull down
            print(f"input_pin:{pin} Input = {input.value()}")




def input_irq(p):
    "Interrupt handler"
    # print(p)
    value = p.value()
    print(f"Input changed, value={value}")


def test_input_irq(input_pin):
    "More advanced, interrupt based input handling"
    input = Pin(input_pin, Pin.IN, Pin.PULL_DOWN) # Think carefully whether you need pull up or pull down
    input.irq(handler=input_irq) # Register irq, you could also consider rising and falling edges c.f. https://docs.micropython.org/en/latest/library/machine.Pin.html

    while True:
        pass # irq handling does the rest in this instance

test_input_poll([16,17,18,19])
