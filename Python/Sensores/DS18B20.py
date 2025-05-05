import glob
import time

class DS18B20Sensor:
    def __init__(self, sensor_id=None):
        try:
            base_dir = '/sys/bus/w1/devices/'
            if sensor_id:
                self.device_file = f'{base_dir}{sensor_id}/w1_slave'
            else:
                device_folders = glob.glob(base_dir + '28*')
                if not device_folders:
                    raise FileNotFoundError("Sensor DS18B20 n�o encontrado.")
                self.device_file = device_folders[0] + '/w1_slave'
            self.failed = False
        except Exception as e:
            print("[ERRO] N�o foi poss�vel inicializar o DS18B20:", e)
            self.device_file = None
            self.failed = True

    def read_raw(self):
        try:
            with open(self.device_file, 'r') as f:
                return f.readlines()
        except Exception as e:
            print("[ERRO] Leitura bruta falhou:", e)
            return []

    def read(self):
        if self.failed or self.device_file is None:
            return None, None
        lines = self.read_raw()
        retry_count = 0
        while lines and lines[0].strip()[-3:] != 'YES':
            time.sleep(0.2)
            lines = self.read_raw()
            retry_count += 1
            if retry_count > 5:
                return None, None
        if lines:
            equals_pos = lines[1].find('t=')
            if equals_pos != -1:
                try:
                    temp_string = lines[1][equals_pos+2:]
                    temp_c = float(temp_string) / 1000.0
                    temp_f = temp_c * 9.0 / 5.0 + 32.0
                    return temp_c, temp_f
                except ValueError:
                    return None, None
        return None, None
