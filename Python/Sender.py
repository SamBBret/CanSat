import json


def verify_value(val):
    return val if val is not None else "N/A"

def convert_data_to_json(inside_temp, inside_hum, accel_values, gyro_values, pi_temp, lat, lon, alt, pressure, temp_bmp, alt_bmp):
   
    sensor_data = {
        "temperature": inside_temp,
        "humidity": inside_hum,
        "acceleration": accel_values,
        "gyro": gyro_values,
        "pi_temp" :  pi_temp,
        "latitude" : lat,
        "longitude" : lon,
        "altitude" : alt,
        "pressure" : pressure,
        "temp_bmp" : temp_bmp, 
        "alt_bmp" : alt_bmp
    }
    
    sensor_data_json = json.dumps(sensor_data)
    
    return sensor_data_json


def send_data(json_data):
    
    print(f"Sending data: {json_data}")
    pass