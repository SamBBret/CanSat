from Sensores.DHT22 import get_dht22
from Interface import update_values, root

def update():
    inside_temp, inside_hum = get_dht22()
    if inside_hum == 0:
        inside_hum = "Erro"
        inside_temp = "Erro"
    
    update_values(inside_temp, inside_hum)
    
    root.after(100, update) 

def setup():
    root.after(100, update) 
    root.mainloop()






if __name__ == "__main__":
    setup()
