from machine import Pin, Timer, I2C
from mcp23017 import MCP23017
from adc import ADC
from numbers import number
import time
from neopixel import Neopixel

pixels = Neopixel(2, 0, 16, "RGBW")
neoBtn = Pin(17, Pin.IN, Pin.PULL_UP)
redled = Pin(18, Pin.OUT)
redled.value(0)
redBtn = Pin(19, Pin.IN, Pin.PULL_UP)

displays = [0b00000001,0b00000010,0b00000100,0b00001000]
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


i2c1 = I2C(1,scl=Pin(15), sda=Pin(14))
addresses = i2c1.scan()
print('i2c1 device on address:')
print(hex(addresses[0]) if len(addresses) > 0 else 'no addresses found')

adc = ADC(i2c1)

i2c0 = I2C(0,scl=Pin(9), sda=Pin(8))
addresses = i2c0.scan()
print('i2c0 devices on address:')
for a in addresses:
    print(hex(a))
# print(hex(addresses[0]) if len(addresses) > 0 else 'no addresses found')

mcp1 = MCP23017(i2c0, 0x20)

mcp1.porta.mode = 0x00
mcp1.portb.mode = 0x00
mcp1.gpio = 0x0f00
mcp1.portb.gpio = 0b00001111

# mcp2 = MCP23017(i2c0, 0x21)
# mcp2.porta.mode = 0b00000000
# mcp2.portb.mode = 0b11111111


def cb(val):
    print('interrupt')
    print(val)

# interrupt pin
# interr = Pin(16, mode=Pin.IN)
# interr.init(mode=interr.IN)
# interr.irq(trigger=interr.IRQ_FALLING, handler=cb)

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
        else:
            counter += 1
    
    lastCLK = clk_encoder.value()
    
    counter = 0 if counter == 10000 else counter
    counter = 9999 if counter == -1 else counter
    
    return counter

def selectDisplay(n):
    global mcp1
    bina = displays[n-1]
    mcp1.portb.gpio = bina
    
def selectNumber(n):
    global mcp1
    mcp1.porta.gpio = ~number[n]
    
def tick(timer):
    global led
    global mcp1
    led.toggle()

def sleep(t=0.00095):
    time.sleep(t)

def number2display(n):
    s = str(n)
    digits = len(s)
    mcp1.porta.gpio = 0xff
    
    if(digits == 1):
        selectDisplay(4)
        selectNumber(int(s))
        sleep()
        mcp1.porta.gpio = 0xff
    elif(digits == 2):
        selectDisplay(3)
        selectNumber(int(s[0]))
        sleep()
        mcp1.porta.gpio = 0xff
        selectDisplay(4)
        selectNumber(int(s[1]))
        sleep()
        mcp1.porta.gpio = 0xff
    elif(digits == 3):
        selectDisplay(2)
        selectNumber(int(s[0]))
        sleep()
        mcp1.porta.gpio = 0xff
        selectDisplay(3)
        selectNumber(int(s[1]))
        sleep()
        mcp1.porta.gpio = 0xff
        selectDisplay(4)
        selectNumber(int(s[2]))
        sleep()
        mcp1.porta.gpio = 0xff
    elif(digits == 4):
        selectDisplay(1)
        selectNumber(int(s[0]))
        sleep()
        mcp1.porta.gpio = 0xff
        selectDisplay(2)
        selectNumber(int(s[1]))
        sleep()
        mcp1.porta.gpio = 0xff
        selectDisplay(3)
        selectNumber(int(s[2]))
        sleep()
        mcp1.porta.gpio = 0xff
        selectDisplay(4)
        selectNumber(int(s[3]))
        sleep()
        mcp1.porta.gpio = 0xff


tim.init(freq=1, mode=Timer.PERIODIC, callback=tick)





while(True):
    encoderValue = readEncoderValue()
    val = adc.read_value()
    voltage = adc.val_to_voltage(val)
    
    formattedVoltage = "{:d}".format(int(voltage*1000))
#     print("ADC Value:", val, formattedVoltage)
    
    number2display(formattedVoltage)
    
    r=int(val/3000)
    
    pixels.set_pixel(0, (3, 5+2*r, 30-r))
    pixels.show()
    
    if(redBtn.value() == 0):
        redled.toggle()
        
    
    
    if(sw_encoder.value() == 0):
        print('pulsando encoder')
    
    if(neoBtn.value() == 0):
        print('pulsando neopixel')
    