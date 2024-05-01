from machine import Pin, Timer, I2C
from mcp23017 import MCP23017
from adc import *
from numbers import number
from button import PixelButton, RedButton, Encoder, PlayButton
import time, random
from neopixel import Neopixel
ADS1115_ADDRESS = 0x48

i2c0 = I2C(0, scl=Pin(17), sda=Pin(16))
addresses = i2c0.scan()

if len(addresses)>0:
    print('i2c0 devices on address:')
    for a in addresses:
        print(hex(a))
    
    print('setting up adc...')
    adc = ADS1115(ADS1115_ADDRESS, i2c=i2c0)
    adc.setMeasureMode(ADS1115_SINGLE)
    
    print('setting up port expander...')
    mcp1 = MCP23017(i2c0, 0x20)
    mcp1.porta.mode = 0x00
    mcp1.portb.mode = 0x00
    mcp1.gpio = 0x0f00
    mcp1.portb.gpio = 0b11111111
    mcp1.porta.gpio = 0xff
else:
    print('no i2c devices found')
    print('this device is ON but doing NOTHING')

#              PTR3210  
displays = [0b00000001,
            0b00000010,
            0b00000100,
            0b00001000]

tim = Timer()

syncIN = Pin(9, Pin.IN, Pin.PULL_UP)
presetIN = machine.ADC(29)
resetIN = Pin(10, Pin.IN, Pin.PULL_UP)

inputs =  {
    'SYNC':syncIN,
    'PRESET':presetIN,
    'RESET':resetIN,
    }

ststpOUT = Pin(15, Pin.OUT)
outA = Pin(28, Pin.OUT)
outB = Pin(27, Pin.OUT)
outC = Pin(26, Pin.OUT)
outD = Pin(25, Pin.OUT)
outA.value(1)
outB.value(1)
outC.value(1)
outD.value(1)

buttonA = RedButton(1,0,0)
buttonB = RedButton(3,2,1)
buttonC = RedButton(7,4,2)
buttonD = RedButton(5,6,3)

encoder = Encoder(18,19,23)
buttonPlay = PlayButton(21)

PXLBTN_0=11   # ALT
PXLBTN_1=13   # CV
PXLBTN_2=20   # PRESET
PXLBTN_3=24   # TEMPO
PXLBTN_4=22   # CHANCE
PXLBTN_5=14   # MUTE
PXLBTN_6=12   # +*/-

alt = PixelButton('ALT',PXLBTN_0, 0)
cv = PixelButton('CV',PXLBTN_1, 1)
preset = PixelButton('PRESET',PXLBTN_2, 2)
tempo = PixelButton('TEMPO',PXLBTN_3, 3)
chance = PixelButton('CHANCE',PXLBTN_4, 4)
mute = PixelButton('MUTE',PXLBTN_5, 5)
mult = PixelButton('+-*/',PXLBTN_6, 6)


buttons = {'A': buttonA,
           'B':buttonB,
           'C':buttonC,
           'D':buttonD,
           'PLAY': buttonPlay,
           'ALT':alt,
           'CV':cv,
           'PRESET':preset,
           'TEMPO':tempo,
           'CHANCE':chance,
           'MUTE':mute,
           '+-*/':mult,
           'ENCODER': encoder}

pixels = Neopixel(7, 0, 8, "RGBW")

for key in buttons:
    b = buttons[key]
    if hasattr(b, 'type'):
        if(b.type == 'pxl'):
            R = int(random.random()*50)
            G = int(random.random()*50)
            B = int(random.random()*50)
            b.color = (R, G, B)
            pixels.set_pixel(b.ledNum,b.color)
            
pixels.show()

outputs= {
    'ST':ststpOUT,
    'A':outA,
    'B':outB,
    'C':outC,
    'D':outD}

def selectDisplay(n):
    mcp1.portb.gpio &= ~(1 << 0)
    mcp1.portb.gpio &= ~(1 << 1)
    mcp1.portb.gpio &= ~(1 << 2)
    mcp1.portb.gpio &= ~(1 << 3)
    
    mcp1.portb.gpio |= (1 << n)

def show(n):
    size = len(n)
    offset = 4 - size
    
    for i in range(size):
        selectDisplay(i+offset)
        mcp1.porta.gpio = number[n[i]]
        sleep(0.002)
        mcp1.porta.gpio = 0xff
   
def tick(timer):
    global values
    global selectedInput
    ststpOUT.toggle()
    
    show(values[selectedInput])

    
def sleep(t=0.001):
    time.sleep(t)

tim.init(freq=40, mode=Timer.PERIODIC, callback=tick)

def readChannel(channel,voltage = False):
    adc.setCompareChannels(channel)
    adc.startSingleMeasurement()
    while adc.isBusy():
        pass
    if voltage:
        value = adc.getResult_V()
    else:
        value = adc.getRawResult()
    
    return value

vA= ""
vB= ""
vC= ""
vD= ""

values = ["0","0","0","0"]
selectedInput = 0
while(True):
    encoder.readValue()
    if 'adc' in globals():
        inA= readChannel(ADS1115_COMP_0_GND,True)
        
        values[0] = "{:d}".format(int(inA*1000))
        
        inB= readChannel(ADS1115_COMP_1_GND,True)
        values[1] = "{:d}".format(int(inB*1000))
        
        inC= readChannel(ADS1115_COMP_2_GND,True)
        values[2] = "{:d}".format(int(inC*1000))
        
        inD= readChannel(ADS1115_COMP_3_GND,True)
        values[3] = "{:d}".format(int(inD*1000))
        
        
        outB.value(inB > 1)
        outC.value(inC > 1)
        outD.value(inD > 1)
        
        print(values)
        
#         print(vA+'\t'+vB+'\t'+vC+'\t'+vD+'\t')
    
    outA.value(syncIN.value())
    
    
    for key in buttons:
        b = buttons[key]
        if(b.btn.value() == 0):
            b.clicked = True
        elif(b.clicked == True):
            b.clicked = False
            if hasattr(b, 'type'):
                if(b.type == 'red'):
                    buttonA.led.value(0)
                    buttonB.led.value(0)
                    buttonC.led.value(0)
                    buttonD.led.value(0)
                    
                    b.led.value(1)
                    selectedInput = b.index
                    
                elif(b.type == 'play'):
                    mcp1.portb.gpio ^= 0b01000000
                elif(b.type == 'pxl'):
                    R = int(random.random()*50)
                    G = int(random.random()*50)
                    B = int(random.random()*50)
                    b.color = (R, G, B)
                    pixels.set_pixel(b.ledNum,b.color)
                    pixels.show()
            print('button ',key)