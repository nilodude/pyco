from machine import Pin, Timer, I2C
from mcp23017 import MCP23017

led = Pin("LED", Pin.OUT)
tim = Timer()

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

def tick(timer):
    global led
    global mcp
    global pos
    global arrlen
    
    led.toggle()
    
    pos = 0 if pos == arrlen-1 else pos + 1 
    mcp.porta.gpio = ~number[pos]
    mcp.portb.gpio ^= 0b00010000
    mcp.portb.gpio ^= pos 

tim.init(freq=1, mode=Timer.PERIODIC, callback=tick)

i2c = I2C(0,scl=Pin(9), sda=Pin(8))
print(i2c.scan())

mcp = MCP23017(i2c, 0x20)

mcp.porta.mode = 0x00
mcp.portb.mode = 0x00

mcp.gpio = 0x0f00
mcp.portb.gpio = 0b00011111

