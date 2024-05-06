from machine import Pin
from rotary_irq import RotaryIRQ

class RedButton:
    def __init__(self, btnPin, ledPin,index):
        self.type = 'red'
        self.btn = Pin(btnPin, Pin.IN, Pin.PULL_UP)
        self.led = Pin(ledPin, Pin.OUT)
        self.led.value(0)
        self.clicked = False
        self.index=index
        
class PlayButton:
    def __init__(self, btnPin):
        self.type = 'play'
        self.btn = Pin(btnPin, Pin.IN, Pin.PULL_UP)
        self.led = 0b01000000
        self.clicked = False

class PixelButton:
    def __init__(self, name, btnPin, ledNum,color=(3,5,30)):
        self.type = 'pxl'
        self.name = name
        self.btn = Pin(btnPin, Pin.IN, Pin.PULL_UP)
        self.ledNum = ledNum
        self.color = color
        self.clicked = False

class Encoder(RotaryIRQ):
     
    def __init__(self, clkPin, dtPin,swPin,minV, maxV):
        self.btn = Pin(swPin, Pin.IN, Pin.PULL_UP)
        self.count = 0
        self.clicked = False
        self.shouldRead = True
        super().__init__(clkPin,dtPin, minV,maxV,reverse=True,range_mode=RotaryIRQ.RANGE_WRAP)
       
    def readValue(self):
        self.count = self.value()
        print('encoder ',self.count)
        return self.count;
        
            