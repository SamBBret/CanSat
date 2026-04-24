from gpiozero import Button
from threading import Lock

class GeigerCounter:
    def __init__(self, pin=27):
        self.pin = pin
        self.pulse_count = 0
        self.lock = Lock()

        self.sensor = Button(self.pin, pull_up=False)
        self.sensor.when_pressed = self._count_pulse

    def _count_pulse(self):
        with self.lock:
            self.pulse_count += 1

    def read(self):
        with self.lock:
            count = self.pulse_count
            self.pulse_count = 0
            return count

    def reset(self):
        with self.lock:
            self.pulse_count = 0

if __name__ == "__main__":
    import time
    geiger = GeigerCounter(pin=27)

    def pulse_callback():
        with geiger.lock:
            geiger.pulse_count += 1
        print("Pulse detected!")


    geiger.sensor.when_pressed = pulse_callback
    print("Geiger counter is running. Waiting for pulses...")

    try:
        while True:
            time.sleep(1)  
    except KeyboardInterrupt:
        print("\nStopped by user.")
    