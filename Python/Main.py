from Sensores.DHT22 import get_dht22
from Interface import update_values, root
from Sensores.mpu9250 import MPU9250
from time import sleep
import os

mode = 0   # terminal = 1 Interface = 0
#mpu = MPU9250()

def update():
    inside_temp, inside_hum = get_dht22()
    #accel_values, gyro_values, mag_values = 0 #mpu.get_all_sensor_data()
    
    if inside_hum == 0:
        inside_hum = "Erro"
        inside_temp = "Erro"
    

    update_values(inside_temp, inside_hum, 0, 0, 0)
    
    root.after(1000, update) 

def setup():
    root.after(1000, update) 
    root.mainloop()
    #mpu.init_sensor()

def terminal_mode():

    inside_temp, inside_hum = get_dht22()
    #accel_values, gyro_values, mag_values = mpu.get_all_sensor_data()

    print("Temperatura:" + str(inside_temp))
    print("Humidade:" + str(inside_hum))
    sleep(0.5)
    os.system('cls' if os.name == 'nt' else 'clear')
    #print(accel_values)
    #print(gyro_values)
    #print(mag_values)


if __name__ == "__main__":
    print(mode)

    if mode == 0:
        setup()
        print("Programa Inicializado")
        sleep(2)
        print("Iniciando os Sensores...")
        while True:
            update()
    else:
        while True:
            terminal_mode()



