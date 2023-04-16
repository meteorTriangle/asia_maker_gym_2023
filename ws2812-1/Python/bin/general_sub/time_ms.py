import time

def get_time_ms():
    timer = time.time_ns() / 1000000
    return int(timer)
