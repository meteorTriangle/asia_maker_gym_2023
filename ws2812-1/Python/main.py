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
    global color_H
    global timer_ref
    color_H += 4.5
    for i in range(31):
        if(LED_enable[i]):
            H = color_H - 5*i
            color = hsv2rgb(H%256, 180, 180)
            LED_DEMO[i]["background"] = color
        else:
            LED_DEMO[i]["background"] = "#000000"
    if(get_time()-timer_ref>40):
        for i in range(30):
            LED_enable[30-i] = LED_enable[(30-i) - 1]
        LED_enable[0] = control_button["state"] != "normal"
        timer_ref = get_time()
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
    print(transdata)
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
            ser.baudrate = 115200
            ser.timeout = 0.01
            ser.write_timeout = 0.1
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
port_refresh_button = ttk.Button(serial_frame, text="重新整理", command=com_list_refresh)
port_refresh_button.pack(side="left")
port_connect_button = ttk.Button(serial_frame, text="連線", command=connect)
port_connect_button.pack(side="left")
port_connect_status = tk.Frame(serial_frame, width=500)
port_connect_status.pack(side="left", fill="both")
time_delay = tk.Label(serial_frame)
time_delay.pack(side="left")

## light control button
control_frame = tk.Frame(root).pack(side="top", fill="x")
control_button = tk.Button(control_frame, text="push", width=25, height=30) ## , command=trigger
control_button.pack(side="left")
DEMO_frame = tk.Frame(control_frame).pack(side="left", fill="x")
LED_DEMO = []
for i in range(31):
    LED_DEMO.append(tk.Frame(DEMO_frame, width=20, height=30, bd=5, relief='groove', background="#000000"))
    LED_DEMO[i].pack(side="left")
run = 1
loop_root()
root.mainloop()

try:
    ser.close()
except:
    pass