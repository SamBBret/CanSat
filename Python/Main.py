from Sensores.DHT22 import get_dht22
#from Sensores.mpu9250 import MPU9250
from Sensores.GPSNEO6 import get_gps_data, send_command_to_gps
from Sensores.BMP280 import get_bmp280_values
from time import sleep
from Sender import send_data, convert_data_to_json, verify_value
from os import popen


wait_time = 1


def setup():
    #mpu = MPU9250()
    send_command_to_gps()


def update(wait_time):
    
    inside_temp, inside_hum = get_dht22()
    accel_values, gyro_values, mag_values = (0,0,0)  # mpu.get_all_sensor_data()
    pi_temp = popen("vcgencmd measure_temp").read().split('=')[1].split("'")[0]
    lat, lon, alt = get_gps_data()
    temp_bmp, pressure, alt_bmp = get_bmp280_values()


    json_data = convert_data_to_json(inside_temp, inside_hum, accel_values, 
                                     gyro_values, mag_values, pi_temp, lat, lon, alt, pressure,
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
