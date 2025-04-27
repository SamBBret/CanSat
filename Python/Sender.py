import json


def verify_value(val):
    return val if val is not None else "N/A"

def convert_data_to_json(inside_temp, inside_hum, accel_x, accel_y, accel_z, gyro_x, gyro_y, gyro_z, pi_temp, lat, lon, alt, pressure, temp_bmp, alt_bmp, time):
   
    sensor_data = {
        "temperature": inside_temp,
        "humidity": inside_hum,
        "accel_x": accel_x,
        "accel_y": accel_y,
        "accel_z": accel_z,
        "gyro_x": gyro_x,
        "gyro_y": gyro_y,
        "gyro_z": gyro_z,
        "pi_temp" : pi_temp,
        "latitude" : lat,
        "longitude" : lon,
        "altitude" : alt,
        "pressure" : pressure,
        "temp_bmp" : temp_bmp, 
        "alt_bmp" : alt_bmp,
        "time_spent" : time
    }
    
    sensor_data_json = json.dumps(sensor_data)
    
    return sensor_data_json

def send_data(json_data):
    
    print(f"Sending data: {json_data}")
    pass