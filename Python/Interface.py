import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from PIL import Image, ImageTk

root = tk.Tk()
root.title("Interface Temporária")
root.configure(bg="white")

root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=3)

title_label = tk.Label(root, text="CanSat", font=("Arial", 24), bg="white")
title_label.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

frame_left = tk.Frame(root, bg="white", bd=2, relief="solid")
frame_left.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

frame_right = tk.Frame(root, bg="white")
frame_right.grid(row=1, column=1, rowspan=3, padx=10, pady=10)

dht22_hum_label = tk.Label(frame_left, text="Humidade: N/A", font=("Arial", 16), bg="white")
dht22_hum_label.grid(row=2, column=0, padx=10, pady=10, sticky="w")

time_label = tk.Label(frame_left, text="Tempo: 0s", font=("Arial", 16), bg="white")
time_label.grid(row=3, column=0, padx=10, pady=10, sticky="w")

dht22_temp_label = tk.Label(frame_left, text="Temperatura Interior: N/A", font=("Arial", 16), bg="white")
dht22_temp_label.grid(row=1, column=0, padx=10, pady=10, sticky="w")


mpu_accel_label = tk.Label(frame_left, text="Acelerômetro: X= N/A, Y= N/A, Z= N/A", font=("Arial", 16), bg="white")
mpu_accel_label.grid(row=4, column=0, padx=10, pady=10, sticky="w")

mpu_gyro_label = tk.Label(frame_left, text="Giroscópio: X= N/A, Y= N/A, Z= N/A", font=("Arial", 16), bg="white")
mpu_gyro_label.grid(row=5, column=0, padx=10, pady=10, sticky="w")

mpu_mag_label = tk.Label(frame_left, text="Magnetômetro: X= N/A, Y= N/A, Z= N/A", font=("Arial", 16), bg="white")
mpu_mag_label.grid(row=6, column=0, padx=10, pady=10, sticky="w")

img = Image.open("Recursos/satimage.jpg")
img = img.resize((250, 250))
photo = ImageTk.PhotoImage(img)

img_label = tk.Label(frame_left, image=photo, bg="white")
img_label.grid(row=0, column=0, padx=10, pady=10)

fig, ax = plt.subplots()
ax.set_title("Temperatura e Humidade")
ax.set_xlabel("Time (s)")
ax.set_ylabel("Value")

ax.set_xlim(0, 10)
ax.set_ylim(-20, 90)

line_temp, = ax.plot([], [], 'r-', label="Temperatura", alpha=0.5)
line_hum, = ax.plot([], [], 'b-', label="Humidade", alpha=0.5)

ax.legend()

time_data = []
temp_data = []
hum_data = []

elapsed_time = 0

def update_values(dht22_temp, dht22_hum, accel, gyro, mag):
    global elapsed_time

    if dht22_hum == 0:
        dht22_temp = "Erro"
        dht22_hum = "Erro"
    
    dht22_temp_label.config(text=f"Temperatura: {dht22_temp}°C")
    dht22_hum_label.config(text=f"Humidade: {dht22_hum}%")
    mpu_accel_label.config(text=f"Acelerômetro: {accel}")
    mpu_gyro_label.config(text=f"Giroscópio: {gyro}")
    mpu_mag_label.config(text=f"Magnetômetro: {mag}")

    time_label.config(text=f"Tempo: {elapsed_time}s")



    time_data.append(elapsed_time)
    temp_data.append(dht22_temp)
    hum_data.append(dht22_hum)

    line_temp.set_data(time_data, temp_data)
    line_hum.set_data(time_data, hum_data)

    ax.relim()
    ax.autoscale_view()

    canvas.draw()

    elapsed_time += 1
    ax.set_xlim(0, elapsed_time)


canvas = FigureCanvasTkAgg(fig, master=frame_right)
canvas.get_tk_widget().grid(row=0, column=0, padx=10, pady=10)


