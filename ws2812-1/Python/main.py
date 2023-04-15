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
ser.baudrate = 250000
ser.timeout = 0.1
ser.write_timeout = 0.1
##ser.set_buffer_size(r)
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
    return port_name

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
            color = hsv2rgb(H%256, 255, 127)
            LED_DEMO[i]["background"] = color
        else:
            LED_DEMO[i]["background"] = "#000000"
    if(get_time()-timer_ref>40):
        for i in range(30):
            LED_enable[30-i] = LED_enable[(30-i) - 1]
        LED_enable[0] = control_button["state"] != "normal"
        timer_ref = get_time()
    if(port_connect["text"] == "斷線"):
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

def search_port():
    '''
    ser_name = com_list_refresh()
    i = 0
    while i < len(ser_name):
        try:
            ser.port = ser_name[i]
            ser.open()
            time.sleep(2.5)
            ser.write("get device nameM".encode("ASCII"))
            time.sleep(0.3)
            if ser.readable():
                recevice = str(ser.read_all(), "ASCII")
                ser.close()
                print(recevice)
                if recevice == "ws2812-1":
                    return ser_name[i]
            ser.close()
        except:
            print("err")
            pass
        i += 1
    try:
        ser.close()
    except:
        pass
    '''
    return 'COM13'

def connect():
    error = 0
    if(ser.is_open == False):
        COM_PORT = search_port()
        print(COM_PORT)
        if COM_PORT == False:
            messagebox.showerror("Error", '請插入Arduino')
            error = 1
        else:
            ser.port = COM_PORT
            try:
                ser.open()
                port_connect["text"] = "斷線"
            except Exception as err:
                error = 1
                messagebox.showerror("error", err)
            print(COM_PORT)
    else:
        ser.close()
        port_connect["text"] = "連線"
        pass


root = tk.Tk()
root.title("WS2812 controller")
root.resizable(False, False)
root.geometry('1000x600')
root.iconbitmap("Python\logo.ico")

com_list_refresh()
print(port_name)

root_menu = tk.Menu(root)
file_menu = tk.Menu(root_menu)
file_menu.add_command(label="open")
file_menu.add_command(label="save")
file_menu.add_command(label="save as")
root_menu.add_cascade(label="file", menu=file_menu)



serial_frame = tk.Frame(root)
serial_frame.pack(side="top", fill="x")
port_connect = tk.Button(serial_frame, text = "連線", command=connect)
port_connect.pack(side="left")
port_connect_status = tk.Frame(serial_frame, width=500)
port_connect_status.pack(side="left", fill="both")
time_delay = tk.Label(serial_frame)
time_delay.pack(side="left")

## light control button
control_frame = tk.Frame(root)
control_frame.pack(side="top", fill="x")
control_button = tk.Button(control_frame, text="push", width=25, height=1) ## , command=trigger
control_button.pack(side="left")
DEMO_frame = tk.Frame(root)
DEMO_frame.pack(side="top", fill="x")
LED_DEMO = []
for i in range(31):
    LED_DEMO.append(tk.Frame(DEMO_frame, width=20, height=30, bd=5, relief='groove', background="#000000"))
    LED_DEMO[i].pack(side="left")
run = 1
root.config(menu=root_menu)
loop_root()
root.mainloop()

try:
    ser.close()
except:
    pass