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

buttonA = RedButton(1,0)
buttonB = RedButton(3,2)
buttonC = RedButton(7,4)
buttonD = RedButton(5,6)
buttonPlay = RedButton(21,0)

redButtons = {'A': buttonA, 'B':buttonB, 'C':buttonC, 'D':buttonD, 'PLAY': buttonPlay}

pixels = Neopixel(1, 0, 16, "RGBW")

neoBtn = PixelButton(PXLBTN_0, 0)
encoder = Encoder(2,3,4)

i2c0 = I2C(0, scl=Pin(17), sda=Pin(16))
addresses = i2c0.scan()

if len(addresses)>0:
    print('i2c0 devices on address:')
    for a in addresses:
        print(hex(a))
    
    print('setting up adc...')
    adc = ADC(i2c0)
    
    print('setting up port expander...')
    mcp1 = MCP23017(i2c0, 0x20)
    mcp1.porta.mode = 0x00
    mcp1.portb.mode = 0x00
    mcp1.gpio = 0x0f00
    mcp1.portb.gpio = 0b00001111
else:
    print('no i2c devices found')
    print('this device is ON but doing NOTHING')


displays = [0b00000001,0b00000010,0b00000100,0b00001000]

def cb(val):
    print('interrupt')
    print(val)

def selectDisplay(n):
    global mcp1
    bina = displays[n-1]
    mcp1.portb.gpio = bina
    
def selectNumber(n):
    global mcp1
    mcp1.porta.gpio = ~number[n]
    
def tick(timer):
    global redButtons
    redButtons['A'].led.toggle()
#     redButtons['B'].led.toggle()
#     redButtons['C'].led.toggle()
    redButtons['D'].led.toggle()
#     redButtons['PLAY'].led.toggle()

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
        sleep(0.002)
        mcp1.porta.gpio = 0xff

tim.init(freq=1, mode=Timer.PERIODIC, callback=tick)
r=0
while(True):
    encoder.readValue()
    if 'adc' in globals():
        val = adc.read_value()
        voltage = adc.val_to_voltage(val)
    
        formattedVoltage = "{:d}".format(int(voltage*1000))
    
        number2display(formattedVoltage)
    
        r=int(val/1500)
        
    neoBtn.color = (3, 4+r, 30-r)
    
    pixels.set_pixel(0, neoBtn.color)
#     pixels.fill(neoBtn.color)
    
    pixels.show()
    
    if(encoder.SW.value() == 0):
        print('pulsandddo encodeeeeer')
    
    if(neoBtn.btn.value() == 0):
        print('pulsando neopixel')
    
    number2display('0666')
      
    for key in redButtons:
        b = redButtons[key]
        if(b.btn.value() == 0):
            b.clicked = True
        elif(b.clicked == True):
            b.clicked = False
            print('button ',key)