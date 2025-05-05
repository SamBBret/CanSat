
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

class MockDS18B20Sensor:
    def __init__(self, sensor_id=None):
        self.failed = False
        self.sensor_id = sensor_id or "28-0000077ba131"
        print(f"[SIMULADO] Sensor DS18B20 iniciado com ID {self.sensor_id}")

    def read(self):
        # Simula uma leitura entre 20 e 30 °C
        temp_c = round(random.uniform(20.0, 30.0), 2)
        temp_f = round(temp_c * 9.0 / 5.0 + 32.0, 2)
        return temp_c, temp_f

class MockMPU6050:
    def __init__(self, *args, **kwargs):
        print("MPU6050 simulado iniciado.")

    def get_accel(self):
        # Simula acelerações em X, Y, Z (g)
        return (
            round(random.uniform(-2.0, 2.0), 2),
            round(random.uniform(-2.0, 2.0), 2),
            round(random.uniform(-2.0, 2.0), 2)
        )

    def get_gyro(self):
        # Simula rotações em X, Y, Z (°/s)
        return (
            round(random.uniform(-250.0, 250.0), 2),
            round(random.uniform(-250.0, 250.0), 2),
            round(random.uniform(-250.0, 250.0), 2)
        )
class MockGPS:
    def __init__(self):
        self.lat = 38.736946
        self.lon = -9.142685
        self.alt = 120.5

    def send_command(self):
        pass

    def start_background_read(self):
        pass

git config --global --no-rebase

