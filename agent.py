import psutil
import socket
import requests
import datetime

BACKEND_URL = "http://127.0.0.1:8000/api/processes/"

def collect_data():
    hostname = socket.gethostname()
    timestamp = datetime.datetime.now().isoformat()

    # --- System details ---
    system_info = {
        "cpu_percent": psutil.cpu_percent(interval=1),
        "memory_total": psutil.virtual_memory().total,
        "memory_used": psutil.virtual_memory().used,
        "memory_percent": psutil.virtual_memory().percent,
    }

    # --- Process details ---
    processes = []
    for proc in psutil.process_iter(['pid', 'name', 'ppid', 'cpu_percent', 'memory_percent']):
        try:
            processes.append(proc.info)
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue

    return {
        "hostname": hostname,
        "timestamp": timestamp,
        "system_info": system_info,
        "processes": processes,
    }

if __name__ == "__main__":
    data = collect_data()
    response = requests.post(BACKEND_URL, json=data)
    print(response.json())
