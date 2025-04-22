import smbus
from time import sleep

# MPU6050 Registers and their Address
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

class MPU6050:
    def __init__(self, bus_num=1, device_address=0x68):
        self.bus = smbus.SMBus(bus_num)
        self.device_address = device_address
        self.accel_scale = 16384.0  # for +/- 2g range
        self.gyro_scale = 131.0     # for +/- 250 deg/sec range
        self.MPU_Init()
        
    def MPU_Init(self):
        """Initialize the MPU6050 sensor"""
        # Write to sample rate register
        self.bus.write_byte_data(self.device_address, SMPLRT_DIV, 7)
        # Write to power management register
        self.bus.write_byte_data(self.device_address, PWR_MGMT_1, 1)
        # Write to Configuration register
        self.bus.write_byte_data(self.device_address, CONFIG, 0)
        # Write to Gyro configuration register
        self.bus.write_byte_data(self.device_address, GYRO_CONFIG, 24)
        # Write to interrupt enable register
        self.bus.write_byte_data(self.device_address, INT_ENABLE, 1)
    
    def read_raw_data(self, addr):
        """Read raw 16-bit value from the specified register"""
        high = self.bus.read_byte_data(self.device_address, addr)
        low = self.bus.read_byte_data(self.device_address, addr+1)
        value = ((high << 8) | low)
        if value > 32768:
            value = value - 65536
        return value
    
    def get_sensor_data(self):
        """Return all sensor data as a dictionary with calibrated values"""
        # Read raw values
        raw_acc_x = self.read_raw_data(ACCEL_XOUT_H)
        raw_acc_y = self.read_raw_data(ACCEL_YOUT_H)
        raw_acc_z = self.read_raw_data(ACCEL_ZOUT_H)
        raw_gyro_x = self.read_raw_data(GYRO_XOUT_H)
        raw_gyro_y = self.read_raw_data(GYRO_YOUT_H)
        raw_gyro_z = self.read_raw_data(GYRO_ZOUT_H)
        
        # Convert to appropriate units
        data = {
            'accel': {
                'x': raw_acc_x / self.accel_scale,
                'y': raw_acc_y / self.accel_scale,
                'z': raw_acc_z / self.accel_scale,
                'units': 'g'
            },
            'gyro': {
                'x': raw_gyro_x / self.gyro_scale,
                'y': raw_gyro_y / self.gyro_scale,
                'z': raw_gyro_z / self.gyro_scale,
                'units': 'deg/s'
            },
            'raw': {
                'accel': {'x': raw_acc_x, 'y': raw_acc_y, 'z': raw_acc_z},
                'gyro': {'x': raw_gyro_x, 'y': raw_gyro_y, 'z': raw_gyro_z}
            }
        }
        return data

    def calibrate_sensor(self, samples=1000):
        """
        Calibrate the sensor by calculating offsets.
        Place the sensor on a flat, level surface during calibration.
        Returns offsets that can be applied to future readings.
        """
        print("Calibrating MPU6050... Keep sensor stationary on flat surface")
        
        # Variables to accumulate offsets
        accel_x_offset = 0
        accel_y_offset = 0
        accel_z_offset = 0
        gyro_x_offset = 0
        gyro_y_offset = 0
        gyro_z_offset = 0
        
        for _ in range(samples):
            # Read raw values
            accel_x = self.read_raw_data(ACCEL_XOUT_H)
            accel_y = self.read_raw_data(ACCEL_YOUT_H)
            accel_z = self.read_raw_data(ACCEL_ZOUT_H)
            gyro_x = self.read_raw_data(GYRO_XOUT_H)
            gyro_y = self.read_raw_data(GYRO_YOUT_H)
            gyro_z = self.read_raw_data(GYRO_ZOUT_H)
            
            # Accumulate offsets
            accel_x_offset += accel_x
            accel_y_offset += accel_y
            accel_z_offset += (accel_z - self.accel_scale)  # Expecting 1g in z-axis
            gyro_x_offset += gyro_x
            gyro_y_offset += gyro_y
            gyro_z_offset += gyro_z
            
            sleep(0.001)
        
        # Calculate average offsets
        offsets = {
            'accel': {
                'x': accel_x_offset / samples,
                'y': accel_y_offset / samples,
                'z': accel_z_offset / samples
            },
            'gyro': {
                'x': gyro_x_offset / samples,
                'y': gyro_y_offset / samples,
                'z': gyro_z_offset / samples
            }
        }
        
        print("Calibration complete. Offsets:", offsets)
        return offsets

# Example usage:
if __name__ == "__main__":
    mpu = MPU6050()
    
    # Calibrate the sensor (recommended on first use)
    # offsets = mpu.calibrate_sensor()
    # You would typically store these offsets and apply them to future readings
    
    # Get sensor data
    data = mpu.get_sensor_data()
    print("Acceleration (g):", data['accel'])
    print("Rotation (deg/s):", data['gyro'])