import json
from Sensores.DHT22 import get_dht22
from Interface import update_values, root
from Sensores.mpu9250 import MPU9250
from time import sleep
import os
import serial

# Provisorio

ser = serial.Serial('/dev/serial0', 9600)




def verify_value(val):
    return val if val is not None else "N/A"


def convert_data_to_json():
   
    inside_temp, inside_hum = get_dht22()
    accel_values, gyro_values, mag_values = (0, 0, 0)

    sensor_data = {
        "temperature": inside_temp,
        "humidity": inside_hum,
        "acceleration": accel_values,
        "gyro": gyro_values,
        "magnetometer": mag_values
    }
    
    sensor_data_json = json.dumps(sensor_data)
    
    return sensor_data_json


def send_data(json_data):
    
    ser.write((json_data + '\n').encode()) 
    #print(f"Sending data: {json_data}")


def update():
    inside_temp, inside_hum = verify_value(get_dht22())
    accel_values, gyro_values, mag_values = verify_value(0)  # mpu.get_all_sensor_data()
    
    update_values(inside_temp, inside_hum, accel_values, gyro_values, mag_values)
    
    root.after(1000, update) 


def setup():
    mpu = MPU9250()
    root.after(1000, update) 
    root.mainloop()


if __name__ == "__main__":
    setup()
    print("Programa Inicializado")
    sleep(2)
    print("Iniciando os Sensores...")

    while True:
        json_data = convert_data_to_json()
        send_data(json_data)
        
        sleep(2)
