import smbus
from time import sleep, time
import statistics

# MPU6050 Registers
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
        self.accel_scale = 16384.0  # ±2g range
        self.gyro_scale = 131.0     # ±250°/s range
        
        # Default calibration offsets (update with calibrate() method)
        self.accel_offsets = {'x': 0, 'y': 0, 'z': 0}
        self.gyro_offsets = {'x': 0, 'y': 0, 'z': 0}
        
        self.MPU_Init()
        self.last_update = time()
        
    def MPU_Init(self):
        """Initialize the MPU6050 sensor"""
        # Wake up the device
        self.bus.write_byte_data(self.device_address, PWR_MGMT_1, 0x00)
        sleep(0.1)
        # Configure sample rate (1kHz/(1+7) = 125Hz)
        self.bus.write_byte_data(self.device_address, SMPLRT_DIV, 7)
        # Disable DLPF (set bandwidth to 260Hz)
        self.bus.write_byte_data(self.device_address, CONFIG, 0x00)
        # Set gyro range to ±250°/s
        self.bus.write_byte_data(self.device_address, GYRO_CONFIG, 0x00)
        # Enable interrupts
        self.bus.write_byte_data(self.device_address, INT_ENABLE, 1)
        sleep(0.1)
    
    def read_raw_data(self, addr):
        """Read raw 16-bit value from register"""
        high = self.bus.read_byte_data(self.device_address, addr)
        low = self.bus.read_byte_data(self.device_address, addr+1)
        value = (high << 8) | low
        return value - 65536 if value > 32768 else value
    
    def calibrate(self, samples=500, threshold=50):
        """
        Auto-calibrate the sensor by collecting samples while stationary.
        Returns True if calibration succeeded.
        """
        print(f"Calibrating MPU6050 with {samples} samples...")
        
        accel_x = []
        accel_y = []
        accel_z = []
        gyro_x = []
        gyro_y = []
        gyro_z = []
        
        # Collect samples
        for _ in range(samples):
            try:
                # Read raw values
                ax = self.read_raw_data(ACCEL_XOUT_H)
                ay = self.read_raw_data(ACCEL_YOUT_H)
                az = self.read_raw_data(ACCEL_ZOUT_H)
                gx = self.read_raw_data(GYRO_XOUT_H)
                gy = self.read_raw_data(GYRO_YOUT_H)
                gz = self.read_raw_data(GYRO_ZOUT_H)
                
                accel_x.append(ax)
                accel_y.append(ay)
                accel_z.append(az)
                gyro_x.append(gx)
                gyro_y.append(gy)
                gyro_z.append(gz)
                
                sleep(0.005)
            except Exception as e:
                print(f"Read error during calibration: {e}")
                return False
        
        # Calculate median values (more robust than mean)
        try:
            # Accelerometer offsets (Z should be ~1g)
            self.accel_offsets['x'] = -statistics.median(accel_x)
            self.accel_offsets['y'] = -statistics.median(accel_y)
            self.accel_offsets['z'] = -(statistics.median(accel_z) - self.accel_scale)
            
            # Gyroscope offsets (should be zero)
            self.gyro_offsets['x'] = -statistics.median(gyro_x)
            self.gyro_offsets['y'] = -statistics.median(gyro_y)
            self.gyro_offsets['z'] = -statistics.median(gyro_z)
            
            # Verify calibration quality
            gyro_stdev = max(statistics.stdev(gyro_x), 
                           statistics.stdev(gyro_y),
                           statistics.stdev(gyro_z))
            
            if gyro_stdev > threshold:
                print(f"Warning: High gyro noise (stdev={gyro_stdev}).")
                return False
                
            print("Calibration successful!")
            print(f"Accel Offsets: {self.accel_offsets}")
            print(f"Gyro Offsets: {self.gyro_offsets}")
            return True
            
        except Exception as e:
            print(f"Calibration failed: {e}")
            return False
    
    def get_sensor_data(self, apply_calibration=True):
        """
        Return calibrated sensor data with timestamps.
        Units: accel in g, gyro in °/s
        """
        try:
            # Read raw values
            raw_acc_x = self.read_raw_data(ACCEL_XOUT_H)
            raw_acc_y = self.read_raw_data(ACCEL_YOUT_H)
            raw_acc_z = self.read_raw_data(ACCEL_ZOUT_H)
            raw_gyro_x = self.read_raw_data(GYRO_XOUT_H)
            raw_gyro_y = self.read_raw_data(GYRO_YOUT_H)
            raw_gyro_z = self.read_raw_data(GYRO_ZOUT_H)
            
            # Apply calibration if enabled
            if apply_calibration:
                raw_acc_x += self.accel_offsets['x']
                raw_acc_y += self.accel_offsets['y']
                raw_acc_z += self.accel_offsets['z']
                raw_gyro_x += self.gyro_offsets['x']
                raw_gyro_y += self.gyro_offsets['y']
                raw_gyro_z += self.gyro_offsets['z']
            
            # Calculate time delta since last reading
            now = time()
            dt = now - self.last_update
            self.last_update = now
            
            return {
                'timestamp': now,
                'dt': dt,
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
            
        except Exception as e:
            print(f"Error reading sensor: {e}")
            return None

    def get_gyro_data():

        mpu_data = mpu.get_sensor_data()
                    
        accel = {
                    'x': round(mpu_data['accel']['x'], 3),
                    'y': round(mpu_data['accel']['y'], 3),
                    'z': round(mpu_data['accel']['z'], 3)
                }
                
        gyro = {
                    'x': round(mpu_data['gyro']['x'], 3),
                    'y': round(mpu_data['gyro']['y'], 3),
                    'z': round(mpu_data['gyro']['z'], 3)
                }
        
        return accel, gyro

# Example usage
if __name__ == "__main__":
    mpu = MPU6050()
    
    # Perform calibration (place sensor flat during this)
    if mpu.calibrate():
        print("Calibration successful!")
    else:
        print("Calibration failed, using default offsets")
    
    # Read data loop
    try:
        while True:
            data = mpu.get_sensor_data()
            if data:
                print("\nAccel (g): X={:.3f}, Y={:.3f}, Z={:.3f}".format(
                    data['accel']['x'], data['accel']['y'], data['accel']['z']))
                print("Gyro (°/s): X={:.3f}, Y={:.3f}, Z={:.3f}".format(
                    data['gyro']['x'], data['gyro']['y'], data['gyro']['z']))
            sleep(0.1)
            
    except KeyboardInterrupt:
        print("\nExiting...")