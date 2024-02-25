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

class Encoder:
     
    def __init__(self, clkPin, dtPin,swPin):
        self.CLK = Pin(clkPin, Pin.IN, Pin.PULL_UP)
        self.DT =Pin(dtPin, Pin.IN, Pin.PULL_UP)
        self.SW = Pin(swPin, Pin.IN, Pin.PULL_UP)
        self.currCLK = 0
        self.count = 0
        self.lastCLK= self.CLK.value()

    def readValue(self):
        currCLK=self.CLK.value()
        dt = self.DT.value()
        
        if(currCLK != self.lastCLK and currCLK == 1):
            if(dt != currCLK):
                self.count -= 1
                print(self.count)
            else:
                self.count += 1
                print(self.count)
        
        self.lastCLK = self.CLK.value()
        
        self.count = 0 if self.count == 10000 else self.count
        self.count = 9999 if self.count == -1 else self.count
                