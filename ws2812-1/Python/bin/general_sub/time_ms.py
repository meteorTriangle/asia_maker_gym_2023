import time
import colorsys

def get_time_ms():
    timer = time.time_ns() / 1000000
    return int(timer)

def hsv2rgb(h, s, v):
    h = h/255
    s = s/255
    v = v/255
    rgb = colorsys.hsv_to_rgb(h, s, v)
    RGB_ = []
    for i in range(3):
        RGB_.append('{:02X}'.format(int(rgb[i]*256)))
    return("#" + "".join(RGB_))