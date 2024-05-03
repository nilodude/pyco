from machine import Pin,PWM
import time

class Output:
    def __init__(self, pin,index):
        self.type = 'main'
#         self.pin = Pin(pin, Pin.OUT)
        self.pin = PWM(Pin(pin))
        self.pin.freq(10)
        self.pin.duty_u16(65535)
        self.index=index
        self.modifier = 1.0 # HARDCODED MODIFIER =1
        self.last_external_clock_at = time.ticks_ms()
        self.last_interval_ms = 0
        self.is_high = False
        self.last_state_change_at = time.ticks_ms()
        
    def calculate_state(self, ms):
        gate_duration_ms = self.last_interval_ms / self.modifier # HARDCODED MODIFIER =1
        hi_lo_duration_ms = gate_duration_ms / 2
        elapsed_ms = time.ticks_diff(ms, self.last_state_change_at)
        
        if elapsed_ms > hi_lo_duration_ms:
            self.last_state_change_at = ms
        
        if self.is_high:
            self.is_high = False
        else:
            self.is_high = True
            self.pin.duty_u16(65535)
                
    def set_output_voltage(self):
        if self.is_high:
            self.pin.duty_u16(65535)
        else:
            self.pin.duty_u16(0)