import time
import board
import adafruit_dht

sensor = adafruit_dht.DHT22(board.D4)

def get_dht22():

    try:
        temperature_c = sensor.temperature
        humidity = sensor.humidity            
        return temperature_c, humidity
    except RuntimeError as error:
        print("Sensor NÃO Encontrado")
        time.sleep(0.2)
        return 0.0, 0.0

    except Exception as error:
        sensor.exit()
        return 0.0, 0.0
        
    time.sleep(0.5)

while True:
    time.sleep(0.5)
    inside_temp, inside_hum = get_dht22()
    #accel_values, gyro_values, mag_values = mpu.get_all_sensor_data()

    print("Temperatura:" + str(inside_temp))
    print("Humidade:" + str(inside_hum))