
import random

class DHT22Sensor:
    def __init__(self): self.failed = False
    def read(self): return round(25 + random.uniform(-2, 2), 2), round(60 + random.uniform(-5, 5), 2)

class MPU6050:
    def get_accel(self): return random.uniform(-1, 1), random.uniform(-1, 1), random.uniform(-1, 1)
    def get_gyro(self): return random.uniform(-90, 90), random.uniform(-90, 90), random.uniform(-90, 90)

class GPS:
    def __init__(self):
        self.lat = 38.7169 + random.uniform(-0.001, 0.001)
        self.lon = -9.1399 + random.uniform(-0.001, 0.001)
        self.alt = 100 + random.uniform(-10, 10)
    def send_command(self): pass
    def start_background_read(self): pass

class BMP280Sensor:
    def __init__(self): self.failed = False
    def read(self): return 24.3, 1013.25, 120

class DS18B20Sensor:
    def __init__(self, sensor_id=''): self.failed = False
    def read(self): return 22.5, None
