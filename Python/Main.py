from datetime import datetime
from time import sleep
from Cam import CAMERA
from os import popen
from LogData import log_data_to_file, set_file, PATH
import serial
import subprocess

wait_time = 5
cam = None

ser = None


def setup():

    timestamp = datetime.utcnow().isoformat()
    set_file()

    global cam
    from LogData import PATH
    cam = CAMERA(PATH)
    cam.start_taking_photos_periodically(5)  # 15 segundos entre fotos!!

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
