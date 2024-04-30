from machine import Pin, Timer, I2C
from mcp23017 import MCP23017
from adc import ADC
from numbers import number
from button import PixelButton, RedButton, Encoder, PlayButton
import time, random
from neopixel import Neopixel

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
outA.value(0)
outB.value(0)
outC.value(0)
outD.value(0)

buttonA = RedButton(1,0)
buttonB = RedButton(3,2)
buttonC = RedButton(7,4)
buttonD = RedButton(5,6)

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
    mcp1.portb.gpio = 0b11111111
else:
    print('no i2c devices found')
    print('this device is ON but doing NOTHING')

#              PTR3210  
displays = [0b00000001,
            0b00000010,
            0b00000100,
            0b00001000]

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
        mcp1.porta.gpio = 0xff
        
        for i in range(4):
            selectDisplay(i)
            mcp1.porta.gpio = number[int(n[i])]
            sleep()
            mcp1.porta.gpio = 0xff  

val = 0
prev = 0
   
def tick(timer):
    global prev
    global val

#     outA.toggle()
#     outB.toggle()
#     outC.toggle()
#     outD.toggle()
    ststpOUT.toggle()
    
    if (prev != val):
        print(val)
        prev = val
    
        
        
def sleep(t=0.003):
    time.sleep(t)

tim.init(freq=20, mode=Timer.PERIODIC, callback=tick)


while(True):
    inA=adc0.read_value() > 12000
    outA.value(inA)
    outB.value(presetIN.read_u16() > 35000)
    outC.value(resetIN.value())
    outD.value(resetIN.value())
    
    encoder.readValue()
    if 'adc0' in globals():
        val = adc2.read_value()
        voltage = adc1.val_to_voltage(val)
        formattedVoltage = "{:04d}".format(int(voltage*1000))
#         print(voltage)
#         number2display(formattedVoltage)
#         r=int(val/1500)
        
#     number2display('8888')

    show(formattedVoltage)

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