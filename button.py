from machine import Pin

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

class Encoder:
     
    def __init__(self, clkPin, dtPin,swPin):
        self.CLK = Pin(clkPin, Pin.IN, Pin.PULL_UP)
        self.DT =Pin(dtPin, Pin.IN, Pin.PULL_UP)
        self.btn = Pin(swPin, Pin.IN, Pin.PULL_UP)
        self.currCLK = 0
        self.count = 1
        self.lastCLK= self.CLK.value()
        self.clicked = False
        self.shouldRead = True

    def readValue(self,minV,maxV):
        currCLK=self.CLK.value()
        dt = self.DT.value()
        
        if(currCLK != self.lastCLK and currCLK == 1):
            if(dt != currCLK):
                self.count -= 1
                self.count = maxV if self.count < minV else self.count
                print('encoder ',self.count)
                self.shouldRead = True
            else:
                self.count += 1
                self.count = minV if self.count > maxV else self.count
                print('encoder ',self.count)
                self.shouldRead = True
        
        self.lastCLK = self.CLK.value()