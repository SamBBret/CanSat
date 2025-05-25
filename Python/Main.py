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

wait_time = 15
mpu = None
dht = None
bmp = None
gps = None
ds1 = None
geiger = None

cam = None

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

    global mpu, dht, bmp, gps, ds1, ltr390, geiger, cam
    from LogData import PATH
    cam = CAMERA(PATH)
    cam.start_taking_photos_periodically(5)  # 15 segundos entre fotos!!

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
        geiger = GeigerCounter(pin=22)
        print("Geiger Counter iniciado no GPIO 22.")
    except Exception as e:
        geiger = None
        print(f"[ERRO] Falha ao inicializar Geiger: {e}")



def update(wait_time):
    
    inside_temp, inside_hum = safe_read(dht, "read") or (None, None)
    external_temp, external_hum = safe_read(ds1, "read") or (None, None)
    gyro_x, gyro_y, gyro_z, accel_x, accel_y, accel_z, mag_x, mag_y, mag_z = safe_read(mpu, "read") or (None,) * 9

    pi_temp = popen("vcgencmd measure_temp").read().split('=')[1].split("'")[0] 
    lat, lon, alt = gps.lat, gps.lon, gps.alt 
    temp_bmp, pressure, alt_bmp = safe_read(bmp, "read") or (None, None, None)
    uv, ambient_light, uvi, lux = safe_read(ltr390, "read") or (None,) * 4

    cpl = safe_read(geiger, "read") or None 
    
    csv_data = convert_data_to_csv(
        inside_temp, inside_hum,
        external_temp, external_hum,
        accel_x, accel_y, accel_z,
        gyro_x, gyro_y, gyro_z,
        mag_x, mag_y, mag_z,
        pi_temp, 
        lat, lon, alt,
        pressure, temp_bmp, alt_bmp,
        uv, ambient_light, uvi, lux,
        cpl
    )

    log_data_to_file(csv_data)
    send_data(csv_data)
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
