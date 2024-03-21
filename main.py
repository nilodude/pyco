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

# pixels = Neopixel(2, 0, 16, "RGBW")
pixels = Neopixel(16*16, 0, 16, "GRB")

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
        sleep(0.002)
        mcp1.porta.gpio = 0xff

tim.init(freq=1, mode=Timer.PERIODIC, callback=tick)

while(True):
    encoder.readValue()

    val = adc.read_value()
    voltage = adc.val_to_voltage(val)
    
    formattedVoltage = "{:d}".format(int(voltage*1000))
    
    number2display(formattedVoltage)
    
    r=int(val/1500)
    neoBtn.color = (3, 4+r, 30-r)
    
    rgbw1 = neoBtn.color
    rgbw2 = (56,20+0.1*r, 8-0.1*r)
    pixels.set_pixel_line_gradient(0, 255, rgbw1, rgbw2) # display parpadea cuando hay que llegar a muchos pixeles, se nota latencia

#     hay que investigar porqué el color (aprox) blanco se consigue con (r,g,b)=(94,60,255) en la matriz 16x16
#     con el r=94, g=60, y bajando el azul de 255 se consigue blanco más cálido, pero al bajar el azul el verde hay que bajarlo un poco tambien
#     pixels.fill((94,50,100))
    
    pixels.show()
    
    if(encoder.SW.value() == 0):
        print('pulsandddo encodeeeeer')
    
    if(neoBtn.btn.value() == 0):
        print('pulsando neopixel')
    