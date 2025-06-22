from machine import Pin, PWM, Timer, I2C
from mcp23017 import MCP23017
from adc import *
from numbers import *
from button import PixelButton, RedButton, Encoder, PlayButton
from output import *
import time, random
from neopixel import Neopixel
from rotary_irq import RotaryIRQ
# hay que estudiarse los bucles de clock_mod.py (https://github.com/Allen-Synthesis/EuroPi/blob/main/software/contrib/clock_mod.py#L248)
# y la forma con la que define los objetos ClockOutput con funciones como setExternalClock y el voltaje de salida con PWM
import rp2
from machine import Pin

@rp2.asm_pio(set_init=rp2.PIO.OUT_LOW)
def pin_onoff():
    
    set(pins, 1)
    set(x, 31) [6]
    label("delay_high")
    nop() [29]
    jmp(x_dec, "delay_high")
    
    
    set(pins, 0)
    set(x, 31) [6]
    label("delay_low")
    nop() [29]
    jmp(x_dec, "delay_low")
    
outA = rp2.StateMachine(1, pin_onoff, freq=2000, set_base=Pin(28))
outA.active(1)

ADS1115_ADDRESS = 0x48

i2c0 = I2C(0, scl=Pin(3), sda=Pin(2))
addresses = i2c0.scan()

if len(addresses)>0:
    print('i2c0 devices on address:')
    for a in addresses:
        print(hex(a))
    
#     print('setting up adc...')
#     adc = ADS1115(ADS1115_ADDRESS, i2c=i2c0)
#     adc.setMeasureMode(ADS1115_SINGLE)
    
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

tim = Timer()
tim2 = Timer()

syncIN = Pin(22, Pin.IN, Pin.PULL_UP)
presetIN = machine.ADC(47)
resetIN = Pin(23, Pin.IN, Pin.PULL_UP)

ststpOUT = Pin(29, Pin.OUT)

# outA = Pin(4)
outB = Pin(5)
outC = Pin(6)
outD = Pin(7)



signals= {
    'inputs' :  {
        'SYNC':syncIN,
        'PRESET':presetIN,
        'RESET':resetIN,
    },
    'outputs': {
        'ST':ststpOUT,
#         'A':outA,
        'B':outB,
#         'C':outC,
#         'D':outD
        }
}
values = ["0","0","0","0","0"]
selectedInput = 0

buttonA = RedButton(1,0,0)
buttonB = RedButton(3,2,1)
buttonC = RedButton(7,4,2)
buttonD = RedButton(5,6,3)

encoder = Encoder(18, 19, 23, 1,4)

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
#################################################
def selectDisplay(n):
    mcp1.portb.gpio &= ~(1 << 0)
    mcp1.portb.gpio &= ~(1 << 1)
    mcp1.portb.gpio &= ~(1 << 2)
    mcp1.portb.gpio &= ~(1 << 3)
    mcp1.portb.gpio |= (1 << n)
    
prevN = "0"
def show(n):  
        size = len(n)
        offset = 4 - size
    
        for i in range(size):
            selectDisplay(i+offset)
            mcp1.porta.gpio = number[n[i]]
            sleep(0.002)
            mcp1.porta.gpio = 0xff
        
def sleep(t=0.001):
    time.sleep(t)
    
def tick(timer):
    show(values[selectedInput])

def ststp(timer):
    ststpOUT.toggle()
#     outA.toggle()
    outB.toggle()


# tim.init(freq=35, mode=Timer.PERIODIC, callback=tick)
# tim2.init(freq=1, mode=Timer.PERIODIC, callback=ststp)

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

elapsed = 0
lastToggle=0
# outA.value(0)
while(True):
    
    values[4] = str(encoder.value())
    now = time.ticks_ms()
    if(selectedInput == 4):
        if(encoder.value() > 2):
            newFreq = 10 * encoder.value() # hardcoded initial 10Hz clock
            print(newFreq)
#             outA.freq(newFreq)
        else:
            newFreq = 2+int(10 / encoder.value())
            print(newFreq)
#             outA.freq(newFreq)
        
    
    if 'adc' in globals():
        inA= readChannel(ADS1115_COMP_0_GND,True)
        
        values[0] = "{:d}".format(int(inA*1000))
        
        inB= readChannel(ADS1115_COMP_1_GND,True)
        values[1] = "{:d}".format(int(inB*1000))
        
        inC= readChannel(ADS1115_COMP_2_GND,True)
        values[2] = "{:d}".format(int(inC*1000))
        
        inD= readChannel(ADS1115_COMP_3_GND,True)
        values[3] = "{:d}".format(int(inD*1000))
        
#         print(values)
        
#         print(vA+'\t'+vB+'\t'+vC+'\t'+vD+'\t')
    
      
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
                    
                    if(key == '+-*/'):
                        selectedInput = 4  # hardcoded encoder count value
#                         outA.freq(outA.freq() * encoder.count)
                        
                    R = int(random.random()*50)
                    G = int(random.random()*50)
                    B = int(random.random()*50)
                    b.color = (R, G, B)
                    pixels.set_pixel(b.ledNum,b.color)
                    pixels.show()
            print('button ',key)
            
    
    elapsed_ms = time.ticks_diff(now,lastToggle)
    if(elapsed_ms > 50):
        lastToggle = time.ticks_ms()

    