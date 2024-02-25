from machine import Pin

class RedButton:
    def __init__(self, btnPin, ledPin):
        self.btn = Pin(btnPin, Pin.IN, Pin.PULL_UP)
        self.led = Pin(ledPin, Pin.OUT)



class PixelButton:
    def __init__(self, btnPin, ledNum,color=(3,5,30)):
        self.btn = Pin(btnPin, Pin.IN, Pin.PULL_UP)
        self.led = ledNum
        self.color = color