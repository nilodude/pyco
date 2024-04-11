from machine import Pin

class RedButton:
    def __init__(self, btnPin, ledPin):
        self.type = 'red'
        self.btn = Pin(btnPin, Pin.IN, Pin.PULL_UP)
        self.led = Pin(ledPin, Pin.OUT)
        self.led.value(0)
        self.clicked = False
        
        
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

class Encoder:
     
    def __init__(self, clkPin, dtPin,swPin):
        self.CLK = Pin(clkPin, Pin.IN, Pin.PULL_UP)
        self.DT =Pin(dtPin, Pin.IN, Pin.PULL_UP)
        self.btn = Pin(swPin, Pin.IN, Pin.PULL_UP)
        self.currCLK = 0
        self.count = 0
        self.lastCLK= self.CLK.value()
        self.clicked = False

    def readValue(self):
        currCLK=self.CLK.value()
        dt = self.DT.value()
        
        if(currCLK != self.lastCLK and currCLK == 1):
            if(dt != currCLK):
                self.count += 1
                self.count = 0 if self.count > 9999 else self.count
                print('encoder ',self.count)
            else:
                self.count -= 1
                self.count = 9999 if self.count < 0 else self.count
                print('encoder ',self.count)
        
        self.lastCLK = self.CLK.value()