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
        print("Sensor NÃ£o Encontrado")
        time.sleep(0.2)
        return 0.0, 0.0

    except Exception as error:
        sensor.exit()
        return 0.0, 0.0
        
    time.sleep(0.5)