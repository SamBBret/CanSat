import serial
import pynmea2

def get_gps_data(port="/dev/ttyAMA0", baudrate=9600, timeout=0.5):
    ser = serial.Serial(port, baudrate=baudrate, timeout=timeout)
    
    while True:
        newdata = ser.readline().decode("utf-8", errors="ignore")
        
        if newdata.startswith("$GPRMC"):
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
                # Assim que temos latitude, longitude e altitude, retornamos os valores
                return lat, lon, alt
            except pynmea2.ParseError:
                continue
