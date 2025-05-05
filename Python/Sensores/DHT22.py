import time
#import board
#import adafruit_dht
from Sensores.MockSensors import MockI2C, MockDHT22

class DHT22Sensor:
    def __init__(self):
        try:
            self.sensor = adafruit_dht.DHT22(pin)
            self.failed = False
        except Exception as e:
            print("[ERRO] Não foi possível inicializar o DHT22:", e)
            self.sensor = None
            self.failed = True

    def read(self):
        if self.failed or self.sensor is None:
            return None, None
        try:
            temperature = self.sensor.temperature
            humidity = self.sensor.humidity
            return temperature, humidity
        except RuntimeError:
            # Erros normais de leitura do DHT
            return None, None
        except Exception as e:
            print("[ERRO CRÍTICO] Problema com o DHT22:", e)
            self.failed = True
            return None, None

    def close(self):
        if self.sensor:
            self.sensor.exit()

