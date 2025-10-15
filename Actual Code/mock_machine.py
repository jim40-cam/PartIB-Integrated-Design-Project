class Pin:
    IN = 0
    PULL_DOWN = 1

    def __init__(self, pin, mode, pull=None):
        self.pin = pin
        self.mode = mode
        self.pull = pull

    def value(self):
        return 0

    def irq(self, handler=None):
        pass