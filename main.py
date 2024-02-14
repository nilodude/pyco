from machine import Pin, Timer, I2C
from mcp23017 import MCP23017

led = Pin("LED", Pin.OUT)
tim = Timer()

clk_encoder = Pin(2, Pin.IN, Pin.PULL_UP)
dt_encoder = Pin(3, Pin.IN, Pin.PULL_UP)
sw_encoder = Pin(4, Pin.IN, Pin.PULL_UP)


currCLK = 0
counter = 0
lastCLK = clk_encoder.value()
lastBtnPres = 0
pushBtn = False

zero = 	0b11101110
one = 	0b00101000
two = 	0b11011010
three = 0b01111010
four= 	0b00111100
five= 	0b01110110
six = 	0b11110110
seven = 0b00101010
eight = 0b11111110
nine = 	0b00111110

number = [zero, one, two, three,four,five, six, seven, eight,nine]
arrlen = len(number)
pos = 0

def readEncoderValue():
    global clk_encoder
    global dt_encoder
    global pushBtn
    global currCLK
    global lastCLK
    global counter
    
    currCLK=clk_encoder.value()
    dt = dt_encoder.value()
    
    if(currCLK != lastCLK and currCLK == 1):
        if(dt != currCLK):
            counter -= 1
            print(counter)
        else:
            counter += 1
            print(counter)
    
    lastCLK = clk_encoder.value()
    
    counter = 0 if counter == 10 else counter
    counter = 9 if counter == -1 else counter
    
    return counter


def tick(timer):
    global led
    led.toggle()

tim.init(freq=1, mode=Timer.PERIODIC, callback=tick)

i2c = I2C(0,scl=Pin(9), sda=Pin(8))

addresses = i2c.scan()
print('i2c device on address:')
print(hex(addresses[0]) if len(addresses) > 0 else 'no addresses found')

mcp = MCP23017(i2c, 0x20)

mcp.porta.mode = 0x00
mcp.portb.mode = 0x00

mcp.gpio = 0x0f00
mcp.portb.gpio = 0b00011111


while(True):
    encoderValue = readEncoderValue()
    
    mcp.porta.gpio = ~number[encoderValue]
    
    if(sw_encoder.value() == 0):
        print('pulsao')
    
    
