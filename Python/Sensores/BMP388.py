import smbus2
import time
import struct

# BMP388 Registers
BMP388_ADDR = 0x76 
BMP388_REG_DATA = 0x04  
BMP388_REG_CTRL_MEAS = 0x01 
BMP388_REG_STATUS = 0x03  

class BMP388Sensor:
    def __init__(self, address=BMP388_ADDR):
        self.address = address
        self.bus = smbus2.SMBus(1) 
        self.failed = False

       
        try:
            self.initialize_sensor()
        except Exception as e:
            self.failed = True
            print(f"[ERRO] Falha ao inicializar BMP388: {e}")

    def initialize_sensor(self):
        
        self.write_register(BMP388_REG_CTRL_MEAS, 0x44) 
        time.sleep(0.1) 

    def read_register(self, reg):
        try:
            return self.bus.read_byte_data(self.address, reg)
        except Exception as e:
            print(f"[ERRO] Falha ao ler o registrador {hex(reg)}: {e}")
            return None

    def write_register(self, reg, value):
        try:
            self.bus.write_byte_data(self.address, reg, value)
        except Exception as e:
            print(f"[ERRO] Falha ao escrever no registrador {hex(reg)}: {e}")

    def read_data(self):
        
        try:
            data = self.bus.read_i2c_block_data(self.address, BMP388_REG_DATA, 6)
            
          
            pressure_raw = struct.unpack('>I', bytes([0] + data[0:3]))[0] 
            temp_raw = struct.unpack('>I', bytes([0] + data[3:6]))[0]  

           
            pressure = pressure_raw / 100 
            temperature = temp_raw / 100 
            altitude = self.calculate_altitude(pressure)

            return temperature, pressure, altitude
        except Exception as e:
            print(f"[ERRO] Falha ao ler os dados do BMP388: {e}")
            return None, None, None

    def calculate_altitude(self, pressure):
        sea_level_pressure = 1013.25
        altitude = 44330 * (1 - (pressure / sea_level_pressure) ** 0.1903)
        return altitude

    def read(self):
        return self.read_data()


if __name__ == "__main__":
    bmp = BMP388Sensor()

    if not bmp.failed:
        while True:
            temperature, pressure, altitude = bmp.read()
            print(f"Temperature: {temperature:.2f} °C")
            print(f"Pressure: {pressure:.2f} hPa")
            print(f"Altitude: {altitude:.2f} meters")
            time.sleep(1)
