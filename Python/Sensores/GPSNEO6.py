import serial
import pynmea2
import threading
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
        self.last_valid_position = (None, None)

    
    def start_background_read(self):
        thread = threading.Thread(target=self._background_loop, daemon=True)
        thread.start()

    def _background_loop(self):
        while True:
            lat, lon, alt = self.read()
            if self.is_valid_coordinate(lat, lon):
                self.lat, self.lon = lat, lon
                self.last_valid_position = (lat, lon)
            elif self.last_valid_position != (None, None):
                self.lat, self.lon = self.last_valid_position
            self.alt = alt

    def is_valid_coordinate(self, lat: float, lon: float) -> bool:
        return (
            lat is not None and lon is not None and
            abs(lat) > 0.001 and abs(lon) > 0.001 and
            -90 <= lat <= 90 and -180 <= lon <= 180
        )

    def read(self) -> Tuple[Optional[float], Optional[float], Optional[float]]:
        try:
            # Temporários para nova leitura
            temp_lat, temp_lon, temp_alt = None, None, None

            for _ in range(10):
                try:
                    newdata = self.ser.readline().decode("utf-8", errors="ignore").strip()
                    if not newdata:
                        continue

                    if newdata.startswith("$GPGLL"):
                        msg = pynmea2.parse(newdata)
                        if self.is_valid_coordinate(msg.latitude, msg.longitude):
                            temp_lat, temp_lon = msg.latitude, msg.longitude
                            self.last_valid_position = (temp_lat, temp_lon)

                    elif newdata.startswith("$GPGGA"):
                        msg = pynmea2.parse(newdata)
                        if msg.gps_qual > 0:
                            temp_alt = msg.altitude

                except (pynmea2.ParseError, UnicodeDecodeError):
                    continue
                except Exception as e:
                    print(f"[WARN] GPS parsing warning: {str(e)}")
                    continue

                # Se tiver nova ou última posição válida + altitude, retorna
                lat = temp_lat or self.last_valid_position[0]
                lon = temp_lon or self.last_valid_position[1]

                if self.is_valid_coordinate(lat, lon) and temp_alt is not None:
                    self.lat, self.lon, self.alt = lat, lon, temp_alt
                    return self.lat, self.lon, self.alt

            # Se nada novo, tenta retornar última válida com antiga altitude
            lat, lon = self.last_valid_position
            if self.is_valid_coordinate(lat, lon):
                return lat, lon, self.alt  # alt pode ser antiga ou None

            return None, None, None  # Nada de útil encontrado

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
