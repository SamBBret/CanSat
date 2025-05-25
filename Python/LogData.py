from datetime import datetime
from threading import Thread
from queue import Queue
import os

log_queue = Queue()
LOG_FILE = None
PATH = None
log_thread = None  

def set_file():
    global PATH, LOG_FILE, log_thread
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    folder_path = timestamp
    PATH = folder_path
    os.makedirs(PATH, exist_ok=True)
    LOG_FILE = os.path.join(PATH, f"{timestamp}_voo_dados.txt")

    log_thread = Thread(target=log_worker, args=(LOG_FILE,), daemon=True)
    log_thread.start()

def log_worker(filename):
    while True:
        json_data = log_queue.get()
        if json_data is None:
            break
        timestamp = datetime.utcnow().isoformat()
        try:
            with open(filename, "a") as f:
                f.write(f"{timestamp} | {json_data}\n")
        except Exception as e:
            print(f"[ERRO] Falha ao gravar dados no ficheiro: {e}")
        log_queue.task_done()

def log_data_to_file(json_data):
    log_queue.put(json_data)

def stop_logging():
    log_queue.put(None)
    if log_thread is not None:
        log_thread.join()
