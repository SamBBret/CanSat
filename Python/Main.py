import json
from Sensores.DHT22 import get_dht22
#from Sensores.mpu9250 import MPU9250
from time import sleep
import os
import serial


def verify_value(val):
    return val if val is not None else "N/A"


def convert_data_to_json():
   
    inside_temp, inside_hum = get_dht22()
    accel_values, gyro_values, mag_values = (0, 0, 0)
    pi_temp = os.popen("vcgencmd measure_temp").read().split('=')[1].split("'")[0]


    sensor_data = {
        "temperature": inside_temp,
        "humidity": inside_hum,
        "acceleration": accel_values,
        "gyro": gyro_values,
        "magnetometer": mag_values,
        "pi_temp" :  pi_temp
    }
    
    sensor_data_json = json.dumps(sensor_data)
    
    return sensor_data_json


def send_data(json_data):
    
    print(f"Sending data: {json_data}")
    pass


def update():
    inside_temp, inside_hum = verify_value(get_dht22())
    accel_values, gyro_values, mag_values = verify_value(0)  # mpu.get_all_sensor_data()


def setup():
    #mpu = MPU9250()
    pass


if __name__ == "__main__":
    setup()
    print("Programa Inicializado")
    sleep(2)
    print("Iniciando os Sensores...")

    while True:

        json_data = convert_data_to_json()
        send_data(json_data)
        sleep(1)
