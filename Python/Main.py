from Sensores.DHT22 import get_dht22
from Interface import update_values, root
from Sensores.mpu9250 import MPU9250
from time import sleep
import os

mode = 0   # terminal = 1 Interface = 0


# Verifical se o sensor retornou uma variavel real
def verify_value(val):
    return val if val is not None else "N/A"



def update():
    inside_temp, inside_hum = verify_value(get_dht22())
    accel_values, gyro_values, mag_values = verify_value(0) #mpu.get_all_sensor_data()
    
    update_values(inside_temp, inside_hum, accel_values, gyro_values, mag_values)
    
    root.after(1000, update) 


def setup():
    
    mpu = MPU9250()
    root.after(1000, update) 
    root.mainloop()

def terminal_mode():

    inside_temp, inside_hum = get_dht22()
  
    print("Temperatura:" + str(inside_temp))
    print("Humidade:" + str(inside_hum))
    sleep(0.5)
    os.system('cls' if os.name == 'nt' else 'clear')
    #print(accel_values)
    #print(gyro_values)
    #print(mag_values)


if __name__ == "__main__":

    setup()
    print("Programa Inicializado")
    sleep(2)
    print("Iniciando os Sensores...")
    while True:
        update()


