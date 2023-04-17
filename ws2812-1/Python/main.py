import tkinter as tk
from tkinter import ttk
from tkinter.constants import *
from tkinter import messagebox
from tkinter import font as tkf
from tkinter import scrolledtext
from tkinter import filedialog
from PIL import Image, ImageTk
import colorsys
import time
import serial
import serial.tools.list_ports_windows
from bin.action_sub import rainbow_flow_frame as rff
from bin.action_sub import gradual_change as gc
import pyaudio

import sounddevice as sd
import numpy as np

volume_norm = 0

def print_sound(indata, outdata, frames, time, status):
    global volume_norm 
    volume_norm = pow(np.linalg.norm(indata)*7, 3.5)
    
    ####print ("|" * int(volume_norm))
'''
with sd.Stream(callback=print_sound):
    sd.sleep(10000)
'''
'''
sound  = True
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
RECORD_SECONDS = 1000
p = pyaudio.PyAudio()
stream = p.open(format = FORMAT,
                channels = CHANNELS,
                rate = RATE,
                input = True,
                input_device_index = 2,
                frames_per_buffer = CHUNK)

stream_data = stream.read(CHUNK)
print(stream_data)

'''
class volume__:
    def __init__(self, LED_count, start_H):
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
        
        self.latest_time = rff.ms.get_time_ms()
        self.ss = sd.Stream(callback=print_sound, device=("rrrStereo Mix (Realtek(R) Audio, MME", None))
        self.ss.start()
    def run(self):
        return_color = []
        global volume_norm 
        ##volume_norm = np.linalg.norm(self.ss.read(1000))*10
        for i in range(self.LED_count):
            self.LED_enable[i] = int(volume_norm) > i
        for i in range(self.LED_count):
            return_color.append(
                rff.ms.hsv2rgb(
                    (self.now_color_H - self.color_diff*i) % 256, 
                    self.color_S * self.LED_enable[i], 
                    self.color_V * self.LED_enable[i]
                )
            )
        self.now_color_H += self.colorchangeSpeed
        return return_color

run = 0
color_H = float(0)
ser = serial.Serial()


com_list_description = []
port_name = []

LED_enable = []
for i in range(31):
    LED_enable.append(False)

def get_time():
        timer = time.time_ns() / 1000000
        return int(timer)

timer_ref = get_time()

def com_list_refresh(arg=None):
    global port_name
    global com_list_description
    port__ = serial.tools.list_ports_windows.comports()
    com_list_description.clear()
    port_name.clear()
    for p in port__:
        port_name.append(p.name)
        com_list_description.append(p.description)
    if(len(com_list_description) == 0):
        com_list_description.append("請選擇序列埠")
    if(run == 1):
        port_menu['menu'].delete(0, 'end')
        for i in com_list_description:
            port_menu['menu'].add_command(label=i, command=tk._setit(port_GUI, i))

def hsv2rgb(h, s, v):
    h = h/255
    s = s/255
    v = v/255
    rgb = colorsys.hsv_to_rgb(h, s, v)
    RGB_ = []
    for i in range(3):
        RGB_.append('{:02X}'.format(int(rgb[i]*256)))
    return("#" + "".join(RGB_))

def loop_root():
    LED___ = vvv.run()
    for i in range(31):
        LED_DEMO[i]["background"] = LED___[i]
    if(port_connect_button["text"] == "斷線"):
        com_list_refresh()
        try:
            COM_PORT_index = port_name.index(ser.port)
            if (port_connect_status["bg"] == "#FF0000"):
                ser.close()
                ser.open()
        except:
            port_connect_status["bg"] = "#FF0000"
            
    else:
        port_connect_status["bg"] = "#FFFFFF"
    color_list = []
    for i in range(31):
        color_list.append(LED_DEMO[i]["bg"])
    transdata = "m"
    transdata += "".join(color_list) + "M"
    if(ser.is_open):
        erf_ = get_time()
        try:
            ser.write(transdata.encode("UTF-8"))
            port_connect_status["bg"] = "#00FF00"
        except:
            port_connect_status["bg"] = "#FF0000"
        time_delay["text"] = str(get_time()-erf_)
    root.after(50, loop_root)

def connect():
    COM_PORT = port_GUI.get()
    error = 0
    if(port_connect_button["text"] == "連線"):
        if COM_PORT == "請選擇序列埠":
            messagebox.showerror("Error", '請選擇序列埠')
            error = 1
        else:
            COM_PORT_index = com_list_description.index(COM_PORT)
            ser.port = port_name[COM_PORT_index]
            ser.baudrate = 250000
            ser.timeout = 0.01
            ser.write_timeout = 0.05
            try:
                ser.open()
            except Exception as err:
                error = 1
                messagebox.showerror("error", err)
            print(port_name[COM_PORT_index])
        if error == 0:
            port_connect_button["text"] = "斷線"
    else:
        port_connect_button["text"] = "連線"
        ser.close()
        pass


root = tk.Tk()
root.title("WS2812 controller")
root.resizable(False, False)
root.geometry('1000x600')
root.iconbitmap("Python/bin/logo.ico")

com_list_refresh()
print(port_name)

root_menu = tk.Menu(root)
file_menu = tk.Menu(root_menu)
file_menu.add_command(label="open")
file_menu.add_command(label="save")
file_menu.add_command(label="save as")
root_menu.add_cascade(label="file", menu=file_menu)

com_list_refresh()
print(com_list_description)

serial_frame = tk.Frame(root)
serial_frame.pack(side="top", fill="x")
port_label = ttk.Label(serial_frame, text="序列埠:").pack(side='left')
port_GUI = tk.StringVar()
port_GUI.set("請選擇序列埠")
port_menu = tk.OptionMenu(serial_frame, port_GUI, *com_list_description, command=com_list_refresh)
port_menu.pack(side="left")
port_refresh_button = ttk.Button(serial_frame, text="重新整理", command=com_list_refresh)
port_refresh_button.pack(side="left")
port_connect_button = ttk.Button(serial_frame, text="連線", command=connect)
port_connect_button.pack(side="left")
port_connect_status = tk.Frame(serial_frame, width=500)
port_connect_status.pack(side="left", fill="both")
time_delay = tk.Label(serial_frame)
time_delay.pack(side="left")


##function selection
function_var = tk.StringVar()
function_var.set('rainbow flow')
function_selector = tk.OptionMenu(serial_frame, function_var, "rainbow flow", "music")
function_selector.pack()

## light control button
control_frame = tk.Frame(root, height=200, bd=2, relief='groove')
control_frame.pack(side="top", fill="x")
rainbow_flow_frame = rff.rainbow_flow_frame(31, control_frame)
rainbow_flow_frame.show()

DEMO_frame = tk.Frame(root)
DEMO_frame.pack(side="bottom", fill="x")
LED_DEMO = []
for i in range(31):
    LED_DEMO.append(tk.Frame(DEMO_frame, width=20, height=30, bd=5, relief='groove', background="#000000"))
    LED_DEMO[i].pack(side="left")
run = 1
root.config(menu=root_menu)
vvv = volume__(31, 85)
loop_root()
root.mainloop()

try:
    ser.close()
except:
    pass
