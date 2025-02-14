# utils.py
from datetime import datetime

def log_message(message):
    """
    Log a message with a timestamp.
    """
    print(f"[{datetime.now()}] {message}")

if __name__ == '__main__':
    log_message("This is a test log message.")
