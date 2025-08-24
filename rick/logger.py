import sys

DEBUG = "--debug" in sys.argv

def log(message: str):
    if DEBUG:
        print(f"[DEBUG] {message}")
