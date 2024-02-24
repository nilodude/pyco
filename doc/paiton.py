from machine import Pin, Timer, I2C
from mcp23017 import MCP23017

led = Pin("LED", Pin.OUT)
tim = Timer()

def tick(timer):
    global led
    led.toggle()

tim.init(freq=2.5, mode=Timer.PERIODIC, callback=tick)

i2c = I2C(1, sda=machine.Pin(6), scl=machine.Pin(7))

mcp = MCP23017(i2c, 0x20)

mcp.mode = 0xfffe
mcp.mode = 65534
mcp.gpio = 0x0001
mcp.gpio = 1