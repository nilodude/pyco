from machine import I2C

class ADC:
    def __init__(self, i2c_bus, address=72):
        self.i2c = i2c_bus
        self.address = address
 
    def read_config(self):
        self.i2c.writeto(self.address, bytearray([1]))
        result = self.i2c.readfrom(self.address, 2)
        return result[0] << 8 | result[1]
 
    def read_value(self):
        self.i2c.writeto(self.address, bytearray([0]))
        result = self.i2c.readfrom(self.address, 2)
        config = self.read_config()
        config &= ~(7 << 12) & ~(7 << 9)
        config |= (4 << 12) | (1 << 9) | (1 << 15)
        config = [int(config >> i & 0xff) for i in (8, 0)]
        self.i2c.writeto(self.address, bytearray([1] + config))
        return result[0] << 8 | result[1]
 
    @staticmethod
    def val_to_voltage(val, max_val=26100, voltage_ref=3.3):
        return val / max_val * voltage_ref