
# MockSensors.py
import random

class MockI2C:
    def __init__(self):
        pass

class MockBMP280:
    def __init__(self, i2c):
        self.sea_level_pressure = 1013.25

    @property
    def temperature(self):
        return round(random.uniform(20.0, 30.0), 2)

    @property
    def pressure(self):
        return round(random.uniform(1000.0, 1020.0), 2)

    @property
    def altitude(self):
        return round(random.uniform(150.0, 170.0), 2)

class MockDHT22:
    def read(self):
        return round(random.uniform(22.0, 28.0), 2), round(random.uniform(40.0, 60.0), 2)

class MockDS18B20:
    def read(self):
        return round(random.uniform(18.0, 25.0), 2), None

class MockMPU6050:
    def get_accel(self):
        return random.uniform(-1, 1), random.uniform(-1, 1), random.uniform(-1, 1)

    def get_gyro(self):
        return random.uniform(-90, 90), random.uniform(-90, 90), random.uniform(-90, 90)

class MockGPS:
    def __init__(self):
        self.lat = 38.736946
        self.lon = -9.142685
        self.alt = 120.5

    def send_command(self):
        pass

    def start_background_read(self):
        pass
