from Sensores.DHT22 import DHT22Sensor 
from Sensores.GY521 import MPU6050
from Sensores.MPU import MPU9250Sensor
from Sensores.GPSNEO6 import GPS
from Sensores.DS18B20 import DS18B20Sensor
from Sensores.LTR390 import LTR390Sensor
from Sensores.Geiger import GeigerCounter
from Sensores.BMP388 import BMP388Sensor
from datetime import datetime
from time import sleep
from Sender import send_data, convert_data_to_csv, verify_value
from LogData import log_data_to_file, set_file, PATH
from Cam import CAMERA
from os import popen
import serial
import subprocess

wait_time = 5
mpu = None
dht = None
bmp = None
gps = None
ds1 = None
geiger = None
cam = None

ser = None

def safe_read(sensor, method_name):
    try:
        if sensor is None:
            return None
        method = getattr(sensor, method_name)
        return method()
    except Exception as e:
        print(f"[ERRO] Falha ao ler {method_name} de {sensor.__class__.__name__}: {e}")
        return None

def setup():

    timestamp = datetime.utcnow().isoformat()
    set_file()

    global mpu, dht, bmp, gps, ds1, ltr390, geiger, cam, ser
    from LogData import PATH
    cam = CAMERA(PATH)
    cam.start_taking_photos_periodically(5)  # 15 segundos entre fotos!!
    try:
        ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)
    except Exception as e:
        ser = None
        print("Serial nâo encontrado")

    try:
        bmp = BMP388Sensor(address=0x76) 
        if bmp.failed:
            print("BMP388 detectado, mas não responde.")
    except Exception as e:
        bmp = None
        print(f"[ERRO] Falha ao inicializar BMP388: {e}")

    try:
        mpu = MPU9250Sensor()
        if mpu.failed:
            print("MPU9250 detectado, mas não responde.")
    except Exception as e:
        mpu = None
        print(f"[ERRO] Falha ao inicializar MPU9250: {e}")

    try:
        dht = DHT22Sensor()
        if dht.failed:
            print("DHT22 detectado, mas não responde.")
    except Exception as e:
        dht = None
        print(f"[ERRO] Falha ao inicializar DHT22: {e}")

    try:
        ds1 = DS18B20Sensor(sensor_id='28-00000ff8c22d')
        if ds1.failed:
            print("DS1 detectado, mas não responde.")
    except Exception as e:
        ds1 = None
        print(f"[ERRO] Falha ao inicializar DS1: {e}")

    try:
        ltr390 = LTR390Sensor()
        if ltr390.failed:
            print("LTR390 detectado, mas não responde.")
    except Exception as e:
        ltr390 = None
        print(f"[ERRO] Falha ao inicializar LTR390: {e}")

    try:
        gps = GPS()
        gps.send_command()
        gps.start_background_read()
        print("GPS iniciado em background.")
    except Exception as e:
        print(f"[ERRO] Falha ao configurar GPS: {e}")
    
    try:
        pin = 27
        geiger = GeigerCounter(pin)
        print(f"Geiger Counter iniciado no GPIO {pin}.")
    except Exception as e:
        geiger = None
        print(f"[ERRO] Falha ao inicializar Geiger: {e}")

def safe(val, factor=1, default=0):
    try:
        return int(float(val) * factor)
    except (TypeError, ValueError):
        return default
    
def get_scaled_cpu_temp() -> int:
    output = subprocess.check_output(["vcgencmd", "measure_temp"]).decode()
    temp = float(output.split('=')[1].split("'")[0])
    return int(temp * 10)

def update(wait_time):
    
    inside_temp, inside_hum = safe_read(dht, "read") or (None, None)
    external_temp, external_hum = safe_read(ds1, "read") or (None, None)
    gyro_x, gyro_y, gyro_z, accel_x, accel_y, accel_z, mag_x, mag_y, mag_z = safe_read(mpu, "read") or (None,) * 9

    pi_temp = get_scaled_cpu_temp()

    lat = gps.lat if gps.lat is not None else 0.0
    lon = gps.lon if gps.lon is not None else 0.0
    alt = gps.alt if gps.alt is not None else 0.0

    temp_bmp, pressure, alt_bmp = safe_read(bmp, "read") or (None, None, None)
    uv, ambient_light, uvi, lux = safe_read(ltr390, "read") or (None,) * 4
    cpl = safe_read(geiger, "read") or None 
    
    gps_sum = (lat * 1_000_000) + (lon * 1_000_000) + (alt * 100)
    data_sum = (
        safe(inside_hum, 100) + safe(inside_temp, 100) +
        safe(external_hum, 100) + safe(external_temp, 100) +
        safe(gyro_x, 1000000) + safe(gyro_y,  1000000) + safe(gyro_z, 1000000) +
        safe(accel_x,1000000) + safe(accel_y,1000000) + safe(accel_z,1000000) +
        safe(pi_temp) +
        safe(temp_bmp, 100) + safe(pressure, 100) +
        safe(uv, 100) + safe(ambient_light, 100) +
        safe(uvi, 100) + safe(lux, 100) + safe(cpl,1)
    )
    # Nao estamos a mandar alt bmp - desnecessarui atualmente
    
    csv_data = convert_data_to_csv(
        gps_sum, data_sum,
        safe(inside_temp, 100), safe(inside_hum, 100),
        safe(external_temp, 100), safe(external_hum, 100),
        safe(accel_x,1000000), safe(accel_y,1000000), safe(accel_z,1000000),
        safe(gyro_x,1000000), safe(gyro_y,1000000), safe(gyro_z,1000000),
        pi_temp,
        lat * 1_000_000, lon * 1_000_000, alt * 100,
        safe(pressure, 100), safe(temp_bmp, 100),
        safe(uv, 100), safe(ambient_light, 100),
        safe(uvi, 100), safe(lux, 100),
        safe(cpl,1)
    )

    log_data_to_file(csv_data)
    if ser != None:
        send_data(ser, csv_data)
    print(csv_data)
    sleep(wait_time)

if __name__ == "__main__":
    setup()
    print("Programa Inicializado")
    sleep(5)
    print("Iniciando os Sensores...")

    try:
        while True:
            update(wait_time)
    except KeyboardInterrupt:
        print("Programa terminado pelo utilizador.")
        if cam:                              
            cam.stop_taking_photos()
