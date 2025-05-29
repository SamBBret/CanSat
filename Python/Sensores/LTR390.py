import time
import board
import adafruit_ltr390

class LTR390Sensor:
    def __init__(self):
        try:
            i2c = board.I2C() 
            self.sensor = adafruit_ltr390.LTR390(i2c)
            self.failed = False
        except Exception as e:
            print("[ERRO] Não foi possível inicializar o LTR390:", e)
            self.sensor = None
            self.failed = True

    def read(self):
        if self.failed or self.sensor is None:
            return None, None, None, None
        try:
            uv = self.sensor.uvs
            ambient_light = self.sensor.light
            uvi = self.sensor.uvi
            lux = self.sensor.lux
            return uv, ambient_light, uvi, lux
        except RuntimeError:
            return None, None, None, None
        except Exception as e:
            print("[ERRO CRÍTICO] Problema com o LTR390:", e)
            self.failed = True
            return None, None, None, None

import time
if __name__ == "__main__":

    ltr = LTR390Sensor()
    while True:
        uv, amb, uvi, lux = ltr.read()
        print("UV: " + str(uv))
        print("Ambiente: " + str(amb))
        print("Uvi: " + str(uvi))
        print("Lux: " + str(lux))

        time.sleep(2)
