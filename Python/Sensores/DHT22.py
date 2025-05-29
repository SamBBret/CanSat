import time
import board
import adafruit_dht

class DHT22Sensor:
    def __init__(self, pin=board.D4):
        try:
            self.sensor = adafruit_dht.DHT22(pin)
            self.failed = False
        except Exception as e:
            print("[ERRO] Não foi possível inicializar o DHT22:", e)
            self.sensor = None
            self.failed = True

    def read(self):
        if self.failed or self.sensor is None:
            print("DHT22 nâo encontrado")
            return None, None
        try:
            temperature = self.sensor.temperature
            humidity = self.sensor.humidity
            return temperature, humidity
        except Exception as e:
            print("[ERRO CRÍTICO] Problema com o DHT22:", e)
            self.failed = True
            return None, None

    def close(self):
        if self.sensor:
            self.sensor.exit()

if __name__ == "__main__":
    import time
    dht = DHT22Sensor()
    while True:
        temp, hum = dht.read()
        print("Temperatura: " + str(temp))
        print("Humidade: " + str(hum))
        time.sleep(2)
        