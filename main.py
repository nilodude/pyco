from machine import Pin, Timer, I2C
from mcp23017 import MCP23017
from adc import ADC
from numbers import number
from button import PixelButton, RedButton, Encoder, PlayButton
import time, random
from neopixel import Neopixel

led = Pin("LED", Pin.OUT)
tim = Timer()

outA = Pin(28, Pin.OUT)
outA.value(0)

PXLBTN_0=11   # ALT
PXLBTN_1=13   # CV
PXLBTN_2=20   # PRESET
PXLBTN_3=24   # TEMPO
PXLBTN_4=22   # CHANCE
PXLBTN_5=14   # MUTE
PXLBTN_6=12   # +*/-

alt = PixelButton('ALT',PXLBTN_0, 0)
mult = PixelButton('+-*/',PXLBTN_6, 6)
encoder = Encoder(18,19,23)

buttonA = RedButton(1,0)
buttonB = RedButton(3,2)
buttonC = RedButton(7,4)
buttonD = RedButton(5,6)
buttonPlay = PlayButton(21)

buttons = {'A': buttonA,
           'B':buttonB,
           'C':buttonC,
           'D':buttonD,
           'PLAY': buttonPlay,
           'ALT':alt,
           '+-*/':mult,
           'ENCODER': encoder}

pixels = Neopixel(7, 0, 8, "RGBW")

i2c0 = I2C(0, scl=Pin(17), sda=Pin(16))
addresses = i2c0.scan()

if len(addresses)>0:
    print('i2c0 devices on address:')
    for a in addresses:
        print(hex(a))
    
    print('setting up adc...')
    adc0 = ADC(i2c0, 0)
    adc1 = ADC(i2c0, 1)
    adc2 = ADC(i2c0, 2)
    adc3 = ADC(i2c0, 3)
    
    print('setting up port expander...')
    mcp1 = MCP23017(i2c0, 0x20)
    mcp1.porta.mode = 0x00
    mcp1.portb.mode = 0x00
    mcp1.gpio = 0x0f00
    mcp1.portb.gpio = 0b01111111
else:
    print('no i2c devices found')
    print('this device is ON but doing NOTHING')

#              PTR3210  
displays = [0b00000001,
            0b00000010,
            0b00000100,
            0b00001000]

def selectDisplay(n):
    global mcp1
    bina = displays[n-1]
    mcp1.portb.gpio = bina
        
def tick(timer):
    global buttons
    mcp1.portb.gpio ^= 0b00110000
    outA.toggle()

def sleep(t=0.00095):
    time.sleep(t)

tim.init(freq=1, mode=Timer.PERIODIC, callback=tick)


while(True):
    encoder.readValue()
    if 'adc0' in globals():
        val = adc0.read_value()
#         print(val)
#         voltage = adc0.val_to_voltage(val)
#         formattedVoltage = "{:d}".format(int(voltage*1000))
#         number2display(formattedVoltage)
#         r=int(val/1500)
        
#     number2display('8888')
    
#     mcp1.porta.gpio = 0b00000000
    
    for key in buttons:
        b = buttons[key]
        if(b.btn.value() == 0):
            b.clicked = True
        elif(b.clicked == True):
            b.clicked = False
            if hasattr(b, 'type'):
                if(b.type == 'red'):
                    b.led.toggle()
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