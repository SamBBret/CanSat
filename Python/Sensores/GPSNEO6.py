import serial
import pynmea2

import serial
import pynmea2

def get_gps_data(port="/dev/ttyAMA0", baudrate=9600, timeout=0.5):
    ser = serial.Serial(port, baudrate=baudrate, timeout=timeout)
    
    lat, lon, alt = None, None, None  # Inicializando as vari�veis antes do loop
    
    while True:
        newdata = ser.readline().decode("utf-8", errors="ignore")
        
        if newdata.startswith("$GPGLL"):
            try:
                msg = pynmea2.parse(newdata)
                lat = msg.latitude
                lon = msg.longitude
            except pynmea2.ParseError:
                continue

        elif newdata.startswith("$GPGGA"):
            try:
                msg = pynmea2.parse(newdata)
                alt = msg.altitude
                # Verifica se lat, lon e alt est�o dispon�veis antes de retornar
                if lat is not None and lon is not None and alt is not None:
                    return lat, lon, alt
            except pynmea2.ParseError:
                continue



def send_command_to_gps(port="/dev/ttyAMA0", baudrate=9600, command=None):

    if command is None:
        command = bytearray([0xB5, 0x62, 0x06, 0x24, 0x24, 0x00, 0xFF, 0xFF, 0x07, 0x03, 0x00, 0x00,
                             0x00, 0x00, 0x10, 0x27, 0x00, 0x00, 0x05, 0x00, 0xFA, 0x00, 0xFA, 0x00,
                             0x64, 0x00, 0x2C, 0x01, 0x00, 0x3C, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                             0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x53, 0x0A])

    # Abre a porta serial
    with serial.Serial(port, baudrate=baudrate, timeout=1) as ser:
        ser.write(command)
        print("Comando enviado para o GPS.")