from ..general_sub import time_ms as ms
import tkinter as tk
class rainbow_flow:
    def __init__(self, LED_count, start_H):
        self.output = []
        self.colorchangeSpeed = 0.25
        self.color_diff = 0.25
        self.flow_period_ms = 20
        self.color_S = 253
        self.color_V = 253
        self.LED_count = LED_count
        self.now_color_H = start_H
        self.LED_enable = []
        for i in range(self.LED_count):
            self.LED_enable.append(0)
        self.latest_time = ms.get_time_ms()
    def run(self, button_state):
        return_color = []
        if (ms.get_time_ms() - self.latest_time) > self.flow_period_ms :
            for i in range(self.LED_count -1):
                self.LED_enable[self.LED_count-1-i] = self.LED_enable[(self.LED_count-1-i) - 1]
            self.LED_enable[0] = button_state
            self.latest_time = ms.get_time_ms()
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


class rainbow_flow_frame:
    def __init__(self, LED_count, parent_Frame):
        self.rainbow_process = rainbow_flow(LED_count, 0)
        self.frame = tk.Frame(parent_Frame)
        self.control_button = tk.Button(self.frame, text="trigger", width=25, height=1)
        self.control_button.pack(side="top")
        self.flow_period_ms_Var = tk.IntVar()
        self.flow_period_ms_Scale = tk.Scale(
            self.frame, 
            variable = self.flow_period_ms_Var, 
            length = 500,
            from_ = 1,
            to = 8,
            resolution = 1,
            label = "流動速度",
            orient = "horizon",
            command = self.flow_period_ms_Scale_change
            )
        self.flow_period_ms_Scale.pack(side="top")

        self.colorchangeSpeed_Var = tk.DoubleVar()
        self.colorchangeSpeed_Scale = tk.Scale(
            self.frame, 
            variable = self.colorchangeSpeed_Var, 
            length = 500,
            from_ = 0.25,
            to = 5,
            resolution = 0.25,
            label="顏色改變速度",
            command = self.colorchangeSpeed_Scale_change,
            orient="horizon"
            )
        self.colorchangeSpeed_Scale.pack(side="top")

        self.color_diff_Var = tk.DoubleVar()
        self.color_diff_Scale = tk.Scale(
            self.frame, 
            variable = self.color_diff_Var, 
            length = 500,
            from_ = 0.25,
            to = 5,
            resolution = 0.25,
            label = "燈株顏色差異",
            command = self.color_diff_Scale_change,
            orient="horizon"
            )
        self.color_diff_Scale.pack(side="top")
    def run(self):
        if (self.control_button["state"] != "normal"):
            state = 1
        else:
            state = 0
        return self.rainbow_process.run(state)
    def show(self):
        self.frame.pack()
    def hide(self):
        self.frame.pack_forget()

    def color_diff_Scale_change(self, value):
        self.rainbow_process.color_diff = float(value)
    def colorchangeSpeed_Scale_change(self, value):
        self.rainbow_process.colorchangeSpeed = float(value)
    def flow_period_ms_Scale_change(self, value):
        self.rainbow_process.flow_period_ms = float(value)*20