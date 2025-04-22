import time
import board
import adafruit_bmp280
from typing import Tuple, Optional

# Initialize with None as default
bmp280 = None


def bmp280_init():
    try:
        i2c = board.I2C()  
        bmp280 = adafruit_bmp280.Adafruit_BMP280_I2C(i2c)
        bmp280.sea_level_pressure = 1013.25
        print("BMP280 initialized successfully")
    except Exception as e:
        print(f"BMP280 initialization failed: {e}")

def get_bmp280_values() -> Tuple[Optional[float], Optional[float], Optional[float]]:

    if bmp280 is None:
        return None, None, None
    
    try:
        temperature = bmp280.temperature
        pressure = bmp280.pressure
        altitude = bmp280.altitude
        return temperature, pressure, altitude
    except Exception as e:
        print(f"Error reading BMP280: {e}")
        return None, None, None