import sounddevice as sd
import numpy as np
from ..general_sub import time_ms as ms
import tkinter as tk

class volume__:
    def __init__(self, LED_count, start_H, device = "speaker"):
        self.output = []
        self.colorchangeSpeed = 0
        self.color_diff = (start_H - 0) / LED_count
        self.flow_period_ms = 20
        self.color_S = 253
        self.color_V = 253
        self.LED_count = LED_count
        self.now_color_H = start_H
        self.LED_enable = []
        for i in range(self.LED_count):
            self.LED_enable.append(0)
        
        self.latest_time = ms.get_time_ms()
        self.ss = sd.Stream(callback=self.print_sound, device=(device, None))
        self.volume_norm = 0
    def run(self):
        return_color = []
        ##volume_norm = np.linalg.norm(self.ss.read(1000))*10
        for i in range(self.LED_count):
            self.LED_enable[i] = int(self.volume_norm) > i
        for i in range(self.LED_count):
            return_color.append(
                ms.hsv2rgb(
                    (self.now_color_H - self.color_diff*i) % 256, 
                    self.color_S * self.LED_enable[i], 
                    self.color_V * self.LED_enable[i]
                )
            )
        self.now_color_H += self.colorchangeSpeed
        return return_color
    
    def print_sound(self, indata, outdata, frames, time, status):
        self.volume_norm = pow(np.linalg.norm(indata)*7, 3.5)

    def set_device(self):
        pass

    def start(self):
        self.ss.start()
    def stop(self):
        self.ss.stop()

    def get_device_list(self) -> list:
        return sd._get_device_id()
    
    ####print ("|" * int(volume_norm))


    class volume_frame:
        def __init__(self) -> None:
            pass