from Python.Sensores.DHT22 import get_dht22
from Interface import update_values
from time import sleep





def setup():
    
    pass


def update_interface_data():
    inside_temp, inside_hum = get_dht22()
    if inside_hum == 0:
        inside_hum = "Erro"
        inside_temp = "Erro"
    update_values(inside_temp, inside_hum)
    


if __name__ == "__main__":

    setup()
    sleep(4)

    while True:
        
        update_interface_data()
