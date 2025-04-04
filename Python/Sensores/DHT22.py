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
        return None, None

    except Exception as error:
        sensor.exit()
        return None, None


