import time
import board
import adafruit_dht
from typing import Tuple, Optional


dht_sensor = None
last_read_time = 0
read_interval = 2.0  

def initialize_dht():
    global dht_sensor
    if dht_sensor is None:
        try:
            dht_sensor = adafruit_dht.DHT22(board.D4)
            print("DHT22 initialized successfully")
            return True
        except Exception as e:
            print(f"DHT22 initialization failed: {e}")
            dht_sensor = None
            return False
    return True

def get_dht22(max_retries: int = 3) -> Tuple[Optional[float], Optional[float]]:

    global last_read_time
    
    if time.monotonic() - last_read_time < read_interval:
        return None, None
    
    for attempt in range(max_retries):
        try:
            temperature = dht_sensor.temperature
            humidity = dht_sensor.humidity
            
            if -40 <= temperature <= 80 and 0 <= humidity <= 100:
                last_read_time = time.monotonic()
                return temperature, humidity
            else:
                print("DHT22 reading out of valid range")
                
        except RuntimeError as e:
            # Common "Cannot read sensor" error, wait and retry
            time.sleep(0.2)
            continue
            
        except Exception as e:
            print(f"DHT22 read error (attempt {attempt+1}): {e}")
            try:
                dht_sensor.exit()
            except:
                pass
            dht_sensor = None
            time.sleep(0.5)
            initialize_dht()
            continue
    
    return None, None
