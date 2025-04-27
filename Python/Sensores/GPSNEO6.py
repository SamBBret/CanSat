import serial
import pynmea2
from typing import Tuple, Optional

class GPS:
    def __init__(self, port="/dev/ttyAMA0", baudrate=9600, timeout=0.5):
        self.port = port
        self.baudrate = baudrate
        self.timeout = timeout
        self.ser = serial.Serial(self.port, baudrate=self.baudrate, timeout=self.timeout)
        self.lat = None
        self.lon = None
        self.alt = None
        self.last_valid_position = (None, None)  # Track last good coordinates

    def is_valid_coordinate(self, lat: float, lon: float) -> bool:
        return (lat is not None and lon is not None 
                and abs(lat) > 0.001 and abs(lon) > 0.001
                and -90 <= lat <= 90 and -180 <= lon <= 180)

    def read(self) -> Tuple[Optional[float], Optional[float], Optional[float]]:
        try:
            while True:
                try:
                    newdata = self.ser.readline().decode("utf-8", errors="ignore").strip()
                    if not newdata:
                        continue

                    if newdata.startswith("$GPGLL"):
                        msg = pynmea2.parse(newdata)
                        if self.is_valid_coordinate(msg.latitude, msg.longitude):
                            self.lat, self.lon = msg.latitude, msg.longitude
                            self.last_valid_position = (self.lat, self.lon)
                        else:
                            print("Invalid GPS location (null island), using last known good position")
                            self.lat, self.lon = self.last_valid_position

                    elif newdata.startswith("$GPGGA"):
                        msg = pynmea2.parse(newdata)
                        
                        if msg.gps_qual > 0:  
                            self.alt = msg.altitude
                            
                            if (self.lat is not None 
                                and self.lon is not None 
                                and self.is_valid_coordinate(self.lat, self.lon)):
                                return self.lat, self.lon, self.alt

                except pynmea2.ParseError:
                    continue
                except UnicodeDecodeError:
                    continue
                except Exception as e:
                    print(f"[WARN] GPS parsing warning: {str(e)}")
                    continue

        except Exception as e:
            print(f"[ERROR] GPS read failure: {str(e)}")
            return None, None, None

    def send_command(self, command=None):
        if command is None:
            command = bytearray([
                0xB5, 0x62, 0x06, 0x24, 0x24, 0x00, 0xFF, 0xFF, 0x07, 0x03,
                0x00, 0x00, 0x00, 0x00, 0x10, 0x27, 0x00, 0x00, 0x05, 0x00,
                0xFA, 0x00, 0xFA, 0x00, 0x64, 0x00, 0x2C, 0x01, 0x00, 0x3C,
                0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                0x00, 0x00, 0x00, 0x00, 0x53, 0x0A
            ])

        try:
            self.ser.write(command)
            print("UBX sent to GPS")
        except Exception as e:
            print(f"[ERROR] Failed to send GPS command: {str(e)}")