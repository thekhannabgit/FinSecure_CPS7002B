# utils/compliance.py
from datetime import datetime
import os

LOG_FILE = os.path.join("data", "audit_log.txt")

class Compliance:
    def __init__(self):
        os.makedirs("data", exist_ok=True)

    def log_event(self, event_type, message):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(LOG_FILE, "a") as log:
            log.write(f"[{timestamp}] {event_type.upper()} - {message}\n")
