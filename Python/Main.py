from Sensores.DHT22 import DHT22Reader
from Sensores.GPSNEO6 import get_gps_data, send_command_to_gps
from Sensores.BMP280 import get_bmp280_values, bmp280_init
from Sensores.GY521 import MPU6050
from time import sleep, time
from Sender import send_data, convert_data_to_json
from os import popen

wait_time = 1
mpu = None

def setup():
    
    bmp280_init()
    DHT22Reader.initialize_sensor()
    
    global mpu
    
    print("Initializing MPU6050...")
    mpu = MPU6050()
    
    # Perform calibration (sensor should be flat and stationary)
    print("Calibrating IMU (keep sensor still)...")
    if not mpu.calibrate(samples=300): 
        print("Warning: IMU calibration may not be accurate")
    
    send_command_to_gps()
    print("All sensors initialized")


def update(wait_time):
    global mpu
    
    try:

        inside_temp, inside_hum = DHT22Reader.read()
        pi_temp = popen("vcgencmd measure_temp").read().split('=')[1].split("'")[0]
        lat, lon, alt = get_gps_data()
        temp_bmp, pressure, alt_bmp = get_bmp280_values()
        accel, gyro = mpu.get_gyro_data()
        
        # Print the calibrated values for verification
        print("\n--- Calibrated IMU Values ---")
        print(f"Accel (g): X={accel['x']:.3f}, Y={accel['y']:.3f}, Z={accel['z']:.3f}")
        print(f"Gyro (Â°/s): X={gyro['x']:.3f}, Y={gyro['y']:.3f}, Z={gyro['z']:.3f}")
        
        # Prepare and send data
        json_data = convert_data_to_json(
            inside_temp, inside_hum, accel, 
            gyro, pi_temp, lat, lon, alt, 
            pressure, temp_bmp, alt_bmp
        )
        
        send_data(json_data)
        
    except Exception as e:
        print(f"Error in update loop: {e}")
    
    sleep(wait_time)

if __name__ == "__main__":
    setup()
    print("Program iniciado")
    print("A calibrar os sensores")
    for i in range(5, 0, -1):
        print(f"\r{i}...", end="", flush=True) 
        sleep(1)


    while True:
        update(wait_time)
