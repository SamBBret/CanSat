from pathlib import Path
from picamera2 import Picamera2
from threading import Thread, Event
from time import sleep
import time

class CAMERA:
    def __init__(self, save_dir):
        self.picam2 = Picamera2()
        self.photo_thread = None
        self.stop_event = Event()
        self.save_dir = Path(save_dir)

        self.still_config = self.picam2.create_still_configuration(
            main={"size": (4608, 2592)}  # 12MP
        )

        self.picam2.configure(self.still_config)
        self.picam2.start()
        sleep(4)  

    def take_photo(self, filename=None):
        if filename is None:
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            filename = f"foto_{timestamp}.jpg"
        full_path = self.save_dir / filename
        self.picam2.capture_file(str(full_path))
        

    def _photo_loop(self, interval_seconds):
        while not self.stop_event.is_set():
            self.take_photo()
            self.stop_event.wait(interval_seconds)

    def start_taking_photos_periodically(self, interval_seconds):
        if self.photo_thread and self.photo_thread.is_alive():
            return
        self.stop_event.clear()
        self.photo_thread = Thread(target=self._photo_loop, args=(interval_seconds,), daemon=True)
        self.photo_thread.start()

    def stop_taking_photos(self):
        if self.photo_thread and self.photo_thread.is_alive():
            self.stop_event.set()
            self.photo_thread.join()
