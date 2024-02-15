from machine import Pin, Timer, I2C
from mcp23017 import MCP23017
import time

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
displays = [0b00000001,0b00000010,0b00000100,0b00001000]


def readEncoderValue():
    global clk_encoder
    global dt_encoder
    global currCLK
    global lastCLK
    global counter
    
    currCLK=clk_encoder.value()
    dt = dt_encoder.value()
    
    if(currCLK != lastCLK and currCLK == 1):
        if(dt != currCLK):
            counter -= 1
#             number2display(counter)
        else:
            counter += 1
#             number2display(counter)
    
    lastCLK = clk_encoder.value()
    
#     counter = 0 if counter == 10 else counter
#     counter = 9 if counter == -1 else counter
    
    return counter

def selectDisplay(n):
    global mcp
    bina = displays[n-1]
    mcp.portb.gpio = bina
    
def selectNumber(n):
    global mcp
    mcp.porta.gpio = ~number[n]
    
def tick(timer):
    global led
    led.toggle()

def number2display(n):
    
    s = str(n)
    
    digits = len(s)
    mcp.porta.gpio = 0xff
    if(digits == 1):
        
        selectDisplay(4)
        selectNumber(int(s))
        mcp.porta.gpio = 0xff
    elif(digits == 2):
        selectDisplay(3)
        selectNumber(int(s[0]))
        mcp.porta.gpio = 0xff
        selectDisplay(4)
        selectNumber(int(s[1]))
    elif(digits == 3):
        selectDisplay(2)
        selectNumber(int(s[0]))
        mcp.porta.gpio = 0xff
        selectDisplay(3)
        selectNumber(int(s[1]))
        mcp.porta.gpio = 0xff
        selectDisplay(4)
        selectNumber(int(s[2]))
    elif(digits == 4):
        selectDisplay(1)
        selectNumber(int(s[0]))
        mcp.porta.gpio = 0xff
        selectDisplay(2)
        selectNumber(int(s[1]))
        mcp.porta.gpio = 0xff
        selectDisplay(3)
        selectNumber(int(s[2]))
        mcp.porta.gpio = 0xff
        selectDisplay(4)
        selectNumber(int(s[3]))
    
    
#     for digit in range(digits):
#         display = 4 - digit
# #         print('display:', display, 'digit:', s[digits-digit-1])
#         selectDisplay(display)
#         mcp.porta.gpio = ~number[int(s[digits-digit-1])]
#         time.sleep(0.005)


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
    
    number2display(encoderValue)
    mcp.gpio = 0x0fff
    
    if(sw_encoder.value() == 0):
        print('pulsando')
    
    
