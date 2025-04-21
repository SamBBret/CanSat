import time
import board

# import digitalio # For use with SPI
import adafruit_bmp280

i2c = board.I2C()  
bmp280 = adafruit_bmp280.Adafruit_BMP280_I2C(i2c)

bmp280.sea_level_pressure = 1013.25

def get_bmp280_values():
    
    temperature = bmp280.temperature
    pressure = bmp280.pressure
    altitude = bmp280.altitude

    return temperature, pressure, altitude


get_bmp280_values()