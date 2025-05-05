#import smbus
from time import sleep

from MockSensors import MockMPU6050 as MPU6050


class MPU6050:

    PWR_MGMT_1   = 0x6B
    SMPLRT_DIV   = 0x19
    CONFIG       = 0x1A
    GYRO_CONFIG  = 0x1B
    INT_ENABLE   = 0x38
    ACCEL_XOUT_H = 0x3B
    ACCEL_YOUT_H = 0x3D
    ACCEL_ZOUT_H = 0x3F
    GYRO_XOUT_H  = 0x43
    GYRO_YOUT_H  = 0x45
    GYRO_ZOUT_H  = 0x47

    def __init__(self, bus_num=1, device_address=0x68):
        self.bus = smbus.SMBus(bus_num)
        self.device_address = device_address
        self.init_sensor()

    def init_sensor(self):
        self.bus.write_byte_data(self.device_address, self.SMPLRT_DIV, 7)
        self.bus.write_byte_data(self.device_address, self.PWR_MGMT_1, 1)
        self.bus.write_byte_data(self.device_address, self.CONFIG, 0)
        self.bus.write_byte_data(self.device_address, self.GYRO_CONFIG, 24)
        self.bus.write_byte_data(self.device_address, self.INT_ENABLE, 1)

    def read_raw_data(self, addr):
        high = self.bus.read_byte_data(self.device_address, addr)
        low = self.bus.read_byte_data(self.device_address, addr + 1)
        value = (high << 8) | low
        if value > 32768:
            value -= 65536
        return value

    def get_accel(self):
        acc_x = self.read_raw_data(self.ACCEL_XOUT_H)
        acc_y = self.read_raw_data(self.ACCEL_YOUT_H)
        acc_z = self.read_raw_data(self.ACCEL_ZOUT_H)
        return (
            acc_x / 16384.0,
            acc_y / 16384.0,
            acc_z / 16384.0
        )

    def get_gyro(self):
        gyro_x = self.read_raw_data(self.GYRO_XOUT_H)
        gyro_y = self.read_raw_data(self.GYRO_YOUT_H)
        gyro_z = self.read_raw_data(self.GYRO_ZOUT_H)
        return (
            gyro_x / 131.0,
            gyro_y / 131.0,
            gyro_z / 131.0
        )



