import serial
import time


def verify_value(val):
    return val if val is not None else "N/A" 

def convert_data_to_csv(*args):
    return ','.join([str(verify_value(val)) for val in args])


 


def send_data(ser, data):
    ser.write((data + '\n').encode('utf-8'))
    print(str(data))

