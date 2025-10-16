from utime import sleep
from machine import Pin

def test_input_poll(input_pin):
    "Simple poll of input"
    input = Pin(input_pin, Pin.IN, Pin.PULL_DOWN) # Think carefully whether you need pull up or pull down

    while True:
        # Poll the value
        value = input.value()
        print(f"input_pin:{input_pin} Input = {value}")
        sleep(0.2)


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


if __name__ == "__main__":
    test_input_poll(input_pin=18)
    test_input_irq(input_pin=18)
    # test_input_irq()

test_input_poll(16)
test_input_poll(17)
test_input_poll(18)
test_input_poll(19)