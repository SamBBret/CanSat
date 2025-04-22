from Sensores.DHT22 import DHT22Sensor 
from Sensores.GY521 import MPU6050
from Sensores.GPSNEO6 import GPS
from Sensores.BMP280 import BMP280Sensor
from time import sleep
from Sender import send_data, convert_data_to_json, verify_value
from os import popen

# Declaração de variaveis gerais
wait_time = 1
mpu = None
dht = None
bmp = None
gps = None

# Verifica se os dados recebidos dos sensores são validos, caso nao o sejam avisa e retorna como None
def safe_read(sensor, method_name):
    try:
        if sensor is None:
            return None
        method = getattr(sensor, method_name)
        return method()
    except Exception as e:
        print(f"[ERRO] Falha ao ler {method_name} de {sensor.__class__.__name__}: {e}")
        return None


# Serve para iniciar todos os sensores, basicamente todo o codigo que deve rodar antes da atualização dos dados começar
def setup():
    global mpu, dht, bmp, gps

    bmp = BMP280Sensor()
    if bmp.failed:
        print("BMP280 não está a responder.")

    try:
        mpu = MPU6050()
    except Exception as e:
        mpu = None
        print(f"[ERRO] Falha ao inicializar MPU6050: {e}")

    try:
        dht = DHT22Sensor()
        if dht.failed:
            print("DHT22 detectado, mas não responde.")
    except Exception as e:
        dht = None
        print(f"[ERRO] Falha ao inicializar DHT22: {e}")

    try:
        gps = GPS
        gps.send_command()
        print("Comando de setup do GPS enviado.")
    except Exception as e:
        print(f"[ERRO] Falha ao configurar GPS: {e}")


# Atualização dos dados e envio de mensagens
def update(wait_time):
    
    inside_temp, inside_hum = safe_read(dht, "read") or (None, None) # Temperaturas Interiores
    accel_values = safe_read(mpu, "get_accel") or (None, None, None) # Aceleração
    gyro_values = safe_read(mpu, "get_gyro") or (None, None, None) # Rotação
    pi_temp = popen("vcgencmd measure_temp").read().split('=')[1].split("'")[0] # Temperatura do Raspberry PI5
    lat, lon, alt = safe_read(gps, "read") or (None, None, None) # Coordenadas do GPS e altitude
    temp_bmp, pressure, alt_bmp = safe_read(bmp, "read") or (None, None, None) # Temperatura, pressão atmosferica e altitude

    json_data = convert_data_to_json(  # Recebe os dados e organiza-os em uma string JSON
        inside_temp, inside_hum,
        accel_values,
        gyro_values,
        pi_temp, 
        lat, lon, alt,
        pressure, temp_bmp, alt_bmp
    )
                        
    send_data(json_data) # Envia os dados
    sleep(wait_time) # Tempo de espera ate repetir novamente, pode ser definido ao chamar a função



if __name__ == "__main__":
    setup()
    print("Programa Inicializado")
    sleep(2)
    print("Iniciando os Sensores...")

    while True:
        update(wait_time)



