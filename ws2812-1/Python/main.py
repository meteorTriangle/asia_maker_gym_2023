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

color_H = float(0)

com_list_description = []

LED_enable = []
for i in range(31):
    LED_enable.append(False)



def get_time():
        timer = time.time_ns() / 1000000
        return int(timer)

timer_ref = get_time()

def com_list_refresh(arg=None):
    global com_list_description
    port__ = serial.tools.list_ports_windows.comports()
    com_list_description.clear()
    for p in port__:
        com_list_description.append(p.description)
    if(len(com_list_description) == 0):
        com_list_description.append("請選擇序列埠")

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
    global color_H
    global timer_ref
    color_H += 0.75
    for i in range(31):
        if(LED_enable[i]):
            H = color_H - 5*i
            color = hsv2rgb(H%256, 180, 180)
            LED_DEMO[i]["background"] = color
        else:
            LED_DEMO[i]["background"] = "#000000"
    if(get_time()-timer_ref>150):
        for i in range(30):
            LED_enable[30-i] = LED_enable[(30-i) - 1]
        LED_enable[0] = control_button["state"] != "normal"
        print(control_button["state"])
        timer_ref = get_time()
    root.after(10, loop_root)

root = tk.Tk()
root.title("WS2812 controller")
root.resizable(False, False)
root.geometry('1000x60')
root.iconbitmap("Python\logo.ico")

com_list_refresh()
print(com_list_description)

serial_frame = tk.Frame(root)
serial_frame.pack(side="top", fill="x")
port_label = ttk.Label(serial_frame, text="序列埠:").pack(side='left')
port_GUI = tk.StringVar()
port_GUI.set("請選擇序列埠")
port_menu = tk.OptionMenu(serial_frame, port_GUI, *com_list_description, command=com_list_refresh)
port_menu.pack(side="left")


## light control button
control_frame = tk.Frame(root).pack(side="top", fill="x")
control_button = tk.Button(control_frame, text="push", width=25, height=30) ## , command=trigger
control_button.pack(side="left")
DEMO_frame = tk.Frame(control_frame).pack(side="left", fill="x")
LED_DEMO = []
for i in range(31):
    LED_DEMO.append(tk.Frame(DEMO_frame, width=20, height=30, bd=5, relief='groove', background="#000000"))
    LED_DEMO[i].pack(side="left")

loop_root()
root.mainloop()