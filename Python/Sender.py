import serial
import time

# Replace these with your actual values or function calls
inside_temp = 24.3
inside_hum = 55.2
external_temp = 18.9
external_hum = 60.1
accel_x = 0.01
accel_y = 0.00
accel_z = 9.81
gyro_x = 0.02
gyro_y = -0.01
gyro_z = 0.00
mag_x = 30.2
mag_y = -47.1
mag_z = 12.5
pi_temp = 50.3
lat = 51.5074
lon = -0.1278
alt = 35.0
pressure = 1013.25
temp_bmp = 20.5
alt_bmp = 32.8
uv = 0.5
ambient_light = 300
uvi = 2.0
lux = 450
cpl = 1.2

def verify_value(val):
    return val if val is not None else "N/A"

def convert_data_to_csv(*args):
    return ','.join([str(verify_value(val)) for val in args])


ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1) 


csv_string = convert_data_to_csv(
    inside_temp, inside_hum, external_temp, external_hum,
    accel_x, accel_y, accel_z, gyro_x, gyro_y, gyro_z,
    mag_x, mag_y, mag_z, pi_temp, lat, lon, alt,
    pressure, temp_bmp, alt_bmp, uv, ambient_light,
    uvi, lux, cpl
)

def send_data(data):

    ser.write((data + '\n').encode())

