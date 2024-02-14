from machine import Pin, Timer, I2C
from mcp23017 import MCP23017

led = Pin("LED", Pin.OUT)
tim = Timer()

def tick(timer):
    global led
    led.toggle()

tim.init(freq=2.5, mode=Timer.PERIODIC, callback=tick)

i2c = I2C(0,scl=Pin(9), sda=Pin(8))
print(i2c.scan())

mcp = MCP23017(i2c, 0x20)

mcp.mode = 0x0000
mcp.portb.gpio = 0b00001111

# cant understand why, portA4 enables display 4 on or off
mcp.porta.gpio = 0b11111000