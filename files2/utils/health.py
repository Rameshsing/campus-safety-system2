import time
import psutil

def system_health_check():
    events = []
    cpu = psutil.cpu_percent()
    mem = psutil.virtual_memory().percent
    if cpu > 90:
        events.append({'timestamp': time.time(), 'type': 'system', 'message': 'High CPU Usage'})
    if mem > 90:
        events.append({'timestamp': time.time(), 'type': 'system', 'message': 'High Memory Usage'})
    return events