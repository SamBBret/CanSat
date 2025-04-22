import time
import board
import adafruit_dht
from typing import Tuple, Optional

class DHT22Reader:
    def __init__(self, pin=board.D4):
        self.pin = pin
        self.sensor = None
        self.last_read_time = 0
        self.read_interval = 2.0  # DHT22 needs 2s between reads
        self.initialize_sensor()

    def initialize_sensor(self):
        """Initialize or reinitialize the sensor"""
        try:
            if self.sensor:
                self.sensor.exit()
            self.sensor = adafruit_dht.DHT22(self.pin)
            return True
        except Exception as e:
            print(f"DHT22 initialization failed: {e}")
            self.sensor = None
            return False

    def read(self, max_retries=3) -> Tuple[Optional[float], Optional[float]]:
        """
        Attempt to read sensor values with retries
        Returns: (temperature, humidity) or (None, None) if failed
        """
        # Check if we should attempt a read (respect cooldown period)
        if time.monotonic() - self.last_read_time < self.read_interval:
            return None, None

        # Ensure sensor is initialized
        if not self.sensor and not self.initialize_sensor():
            return None, None

        # Attempt reading with retries
        for attempt in range(1, max_retries + 1):
            try:
                temperature = self.sensor.temperature
                humidity = self.sensor.humidity
                
                # Validate readings
                if -40 <= temperature <= 80 and 0 <= humidity <= 100:
                    self.last_read_time = time.monotonic()
                    return temperature, humidity
                else:
                    print("DHT22 reading out of valid range")
                    
            except RuntimeError as e:
                # Common "Cannot read sensor" error
                if attempt < max_retries:
                    time.sleep(0.5)
                continue
                
            except Exception as e:
                print(f"DHT22 read error (attempt {attempt}): {e}")
                self.sensor = None  # Force reinitialization next time
                if attempt < max_retries:
                    time.sleep(0.5)
                continue
        
        return None, None