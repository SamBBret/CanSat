from Sensores.DHT22 import get_dht22
#from Sensores.mpu9250 import MPU9250
from Sensores.GPSNEO6 import get_gps_data, send_command_to_gps
from Sensores.BMP280 import get_bmp280_values
from time import sleep
from Sender import send_data, convert_data_to_json, verify_value
from os import popen
from Sensores.GY521 import MPU6050

wait_time = 1
global mpu

def setup():
    mpu = MPU6050()
    send_command_to_gps()


def update(wait_time):
    
    inside_temp, inside_hum = get_dht22()
    pi_temp = popen("vcgencmd measure_temp").read().split('=')[1].split("'")[0]
    lat, lon, alt = get_gps_data()
    temp_bmp, pressure, alt_bmp = get_bmp280_values()
    mpu_data = mpu.get_sensor_data()
    accel_values = mpu_data['accel']
    gyro_values = mpu_data['gyro']

    json_data = convert_data_to_json(inside_temp, inside_hum, accel_values, 
                                     gyro_values, pi_temp, lat, lon, alt, pressure,
                                     temp_bmp, alt_bmp)
    send_data(json_data)
    
    sleep(wait_time)


if __name__ == "__main__":
    setup()
    print("Programa Inicializado")
    sleep(2)
    print("Iniciando os Sensores...")

    while True:
        update(wait_time)
