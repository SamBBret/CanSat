from datetime import datetime
from time import sleep
from Cam import CAMERA
from os import popen
from LogData import log_data_to_file, set_file, PATH
import serial
import subprocess
import time

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

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Programa terminado pelo utilizador.")
        if cam:                              
            cam.stop_taking_photos()
