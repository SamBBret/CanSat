import serial
import pynmea2

class GPS:
    def __init__(self, port="/dev/ttyAMA0", baudrate=9600, timeout=0.5):
        self.port = port
        self.baudrate = baudrate
        self.timeout = timeout
        self.ser = serial.Serial(self.port, baudrate=self.baudrate, timeout=self.timeout)
        self.lat = None
        self.lon = None
        self.alt = None

    def read(self):
        try:
            while True:
                newdata = self.ser.readline().decode("utf-8", errors="ignore")

                if newdata.startswith("$GPGLL"):
                    try:
                        msg = pynmea2.parse(newdata)
                        self.lat = msg.latitude
                        self.lon = msg.longitude
                    except pynmea2.ParseError:
                        continue

                elif newdata.startswith("$GPGGA"):
                    try:
                        msg = pynmea2.parse(newdata)
                        self.alt = msg.altitude
                        if self.lat is not None and self.lon is not None and self.alt is not None:
                            return self.lat, self.lon, self.alt
                    except pynmea2.ParseError:
                        continue
        except Exception as e:
            print(f"[ERRO] Falha ao ler dados GPS: {e}")
            return None, None, None

    def send_command(self, command=None):

        if command is None:
            command = bytearray([0xB5, 0x62, 0x06, 0x24, 0x24, 0x00, 0xFF, 0xFF, 0x07, 0x03, 0x00, 0x00,
                                 0x00, 0x00, 0x10, 0x27, 0x00, 0x00, 0x05, 0x00, 0xFA, 0x00, 0xFA, 0x00,
                                 0x64, 0x00, 0x2C, 0x01, 0x00, 0x3C, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                                 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x53, 0x0A])

        try:
            with serial.Serial(self.port, baudrate=self.baudrate, timeout=1) as ser:
                ser.write(command)
                print("Comando enviado para o GPS.")
        except Exception as e:
            print(f"[ERRO] Falha ao enviar comando para o GPS: {e}")
