import tkinter as tk

root = tk.Tk()
root.title("Interface Temporaria")

dht22_temp_label = tk.Label(root, text="Temperatura Interior: N/A", font=("Arial", 16))
dht22_temp_label.grid(row=1, column=0, padx=10, pady=10)

dht22_hum_label = tk.Label(root, text="Humidade: N/A", font=("Arial", 16))
dht22_hum_label.grid(row=2, column=0, padx=10, pady=10)


def update_values(dht22_temp, dht22_hum, ):
    
    
    dht22_temp_label.config(text=f"Temperatura Interior: {dht22_temp}")
    dht22_hum_label.config(text=f"Humidade: {dht22_hum}")

    
