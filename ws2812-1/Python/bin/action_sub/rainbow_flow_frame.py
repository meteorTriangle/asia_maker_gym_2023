from ..general_sub import time_ms as ms
class rainbow_flow:
    def __init__(self, LED_count, start_H):
        self.output = []
        self.colorchangeSpeed = 4.5
        self.color_diff = 5
        self.flow_period_ms = 40
        self.color_S = 253
        self.color_V = 253
        self.LED_count = LED_count
        self.now_color_H = start_H
        self.LED_enable = []
        for i in range(self.LED_count):
            self.LED_enable.append(0)
        self.latest_time = ms.get_time_ms()
    def run(self, button_state):
        if (ms.get_time_ms() - self.latest_time) > self.flow_period_ms :
            for i in range(self.LED_count -1):
                self.LED_enable[self.LED_count-1-i] = self.LED_enable[(self.LED_count-1-i) - 1]
            self.LED_enable = button_state
        