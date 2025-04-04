import smbus2
import numpy as np

# MPU9250 I2C addresses
MPU9250_ADDR = 0x68
MAGNETOMETER_ADDR = 0x0C

# MPU9250 Registers
PWR_MGMT_1 = 0x6B
ACCEL_XOUT_H = 0x3B
GYRO_XOUT_H = 0x43
TEMP_OUT_H = 0x41
MAGNETOMETER_XOUT_L = 0x03

class MPU9250:
    def __init__(self, bus=1, address=MPU9250_ADDR):
        self.bus = smbus2.SMBus(bus)
        self.address = address
        self.calibration_offsets = {
            "accel": np.array([0, 0, 0]),  # Example: [0, 0, 0]
            "gyro": np.array([0, 0, 0]),   # Example: [0, 0, 0]
            "mag": np.array([0, 0, 0])     # Example: [0, 0, 0]
        }
        self.init_sensor()

    def init_sensor(self):
        # Wake up MPU9250
        self.bus.write_byte_data(self.address, PWR_MGMT_1, 0)

    def read_raw_data(self, reg_addr):
        high = self.bus.read_byte_data(self.address, reg_addr)
        low = self.bus.read_byte_data(self.address, reg_addr + 1)
        val = ((high << 8) | low)
        if val >= 0x8000:
            val = -(65536 - val)
        return val

    def read_accel_data(self):
        ax = self.read_raw_data(ACCEL_XOUT_H)
        ay = self.read_raw_data(ACCEL_XOUT_H + 2)
        az = self.read_raw_data(ACCEL_XOUT_H + 4)
        return np.array([ax, ay, az]) - self.calibration_offsets["accel"]

    def read_gyro_data(self):
        gx = self.read_raw_data(GYRO_XOUT_H)
        gy = self.read_raw_data(GYRO_XOUT_H + 2)
        gz = self.read_raw_data(GYRO_XOUT_H + 4)
        return np.array([gx, gy, gz]) - self.calibration_offsets["gyro"]

    def read_magnetometer_data(self):
        # Read raw magnetometer data (assumes magnetometer is initialized)
        mx = self.bus.read_byte_data(MAGNETOMETER_ADDR, MAGNETOMETER_XOUT_L)
        my = self.bus.read_byte_data(MAGNETOMETER_ADDR, MAGNETOMETER_XOUT_L + 2)
        mz = self.bus.read_byte_data(MAGNETOMETER_ADDR, MAGNETOMETER_XOUT_L + 4)
        return np.array([mx, my, mz]) - self.calibration_offsets["mag"]

    def read_temperature(self):
        temp = self.read_raw_data(TEMP_OUT_H)
        temperature = temp / 340.0 + 36.53  # Temperature in Celsius
        return temperature

    def get_all_sensor_data(self):
        # Retrieve all sensor data and return separate variables
        accel_data = self.read_accel_data()
        gyro_data = self.read_gyro_data()
        mag_data = self.read_magnetometer_data()
        temperature = self.read_temperature()

        # Return all values as separate variables
        return accel_data[0], accel_data[1], accel_data[2], \
               gyro_data[0], gyro_data[1], gyro_data[2], \
               mag_data[0], mag_data[1], mag_data[2], \
               temperature

    def calibrate(self):
        # Apply custom calibration routines based on your setup
        pass
