from machine import Pin, Timer, I2C
from mcp23017 import MCP23017
from adc import ADC
from numbers import number
from button import PixelButton, RedButton, Encoder
import time
from neopixel import Neopixel

led = Pin("LED", Pin.OUT)
tim = Timer()

PXLBTN_0=17
PXLBTN_1=0
PXLBTN_2=0
PXLBTN_3=0
PXLBTN_4=0
PXLBTN_5=0
PXLBTN_6=0

pixels = Neopixel(2, 0, 16, "RGBW")

neoBtn = PixelButton(PXLBTN_0, 0)
encoder = Encoder(2,3,4)

i2c0 = I2C(0,scl=Pin(9), sda=Pin(8))
addresses = i2c0.scan()
print('i2c0 devices on address:')
for a in addresses:
    print(hex(a))

adc = ADC(i2c0)

mcp1 = MCP23017(i2c0, 0x20)

mcp1.porta.mode = 0x00
mcp1.portb.mode = 0x00
mcp1.gpio = 0x0f00
mcp1.portb.gpio = 0b00001111

displays = [0b00000001,0b00000010,0b00000100,0b00001000]

def cb(val):
    print('interrupt')
    print(val)

# def readEncoderValue():
#     global encoder
    
#     currCLK=encoder.CLK.value()
#     dt = encoder.DT.value()
    
#     if(currCLK != encoder.lastCLK and currCLK == 1):
#         if(dt != currCLK):
#             encoder.count -= 1
#             print(encoder.count)
#         else:
#             encoder.count += 1
#             print(encoder.count)
    
#     encoder.lastCLK = encoder.CLK.value()
    
#     encoder.count = 0 if encoder.count == 10000 else encoder.count
#     encoder.count = 9999 if encoder.count == -1 else encoder.count
    

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

def rev(s):
    r = ""
    for c in s:
        r = c+r
    return r

def number2display(n):
    s = rev(str(n))
    digits = len(s)
    mcp1.porta.gpio = 0xff
    
    for digit in range(digits):
        selectDisplay(4 - digit)
        selectNumber(int(s[digit]))
        sleep()
        mcp1.porta.gpio = 0xff


tim.init(freq=1, mode=Timer.PERIODIC, callback=tick)


while(True):
    encoder.readValue()

    val = adc.read_value()
    voltage = adc.val_to_voltage(val)
    
    formattedVoltage = "{:d}".format(int(voltage*1000))
    
    number2display(formattedVoltage)
    
    r=int(val/1500)
    neoBtn.color = (3, 5+2*r, 30-r)
    pixels.set_pixel(0, neoBtn.color)
    pixels.show()
    
        
    if(encoder.SW.value() == 0):
        print('pulsandddo encodeeeeer')
    
    if(neoBtn.btn.value() == 0):
        print('pulsando neopixel')
    