import time
import board
import adafruit_bmp280


class BMP280Sensor:
    def __init__(self, sea_level_pressure=1013.25):
        try:
            i2c = board.I2C()
            self.bmp280 = adafruit_bmp280.Adafruit_BMP280_I2C(i2c)
            self.bmp280.sea_level_pressure = sea_level_pressure
            self.failed = False
            print("BMP280 inicializado com sucesso.")
        except Exception as e:
            print(f"Erro ao inicializar BMP280: {e}")
            self.bmp280 = None
            self.failed = True

    def read(self):
        if self.bmp280 is None:
            return None, None, None

        try:
            temperature = self.bmp280.temperature
            pressure = self.bmp280.pressure
            altitude = self.bmp280.altitude
            return temperature, pressure, altitude
        except Exception as e:
            print(f"Falha ao ler dados do BMP280: {e}")
            return None, None, None
