#### Serial
import serial
import serial.tools.list_ports_windows
#### GUI
import tkinter as tk
from tkinter import ttk
from tkinter.constants import *
from tkinter import messagebox
from tkinter import font as tkf
from tkinter import scrolledtext
from tkinter import filedialog
from PIL import Image, ImageTk
import time
import os

self_path = os.path.dirname(__file__) + "\\"
com_list_description = ['']
com_list_name = []
run = 0
BAUD_RATES = 1000000
ser = serial.Serial()

def port_refresh():
    ### com port read
    com_list_description.clear()
    com_list_name.clear()
    ports = serial.tools.list_ports_windows.comports()
    for p in ports:
        com_list_description.append(p.description)
        com_list_name.append(p.name)
        print(p.description)
        print(p.name)
    if len(ports) == 0:
        com_list_description.append("無")
    print(len(ports), 'ports found')
    
    ###
    if len(ports) == 0:
        messagebox.showinfo("Error", "請插入Arduino")
    if run == 1:
        port_menu['menu'].delete(0, 'end')

        for i in com_list_description:
            port_menu['menu'].add_command(label=i, command=tk._setit(port_GUI, i))

def loop_():
    root.after(30, loop_)

def connect():
    COM_PORT = port_GUI.get()
    ser.baudrate = BAUD_RATES
    if COM_PORT == '請選擇序列埠':
        messagebox.showinfo("Error", '請選擇序列埠')
    else:
        COM_PORT_index = com_list_description.index(COM_PORT)
        print(com_list_name[COM_PORT_index])
    ser.port = com_list_name[COM_PORT_index]
    ser.timeout = 0.01
    ser.write_timeout = 0.01
    try:
        ser.open()
        err_state = False
    except E in Exception:
        err_state = True
        err = E
    if(err_state == False):
        messagebox.showinfo("連線成功", "連線成功")
        com_connect['text'] = "斷線"
        com_connect['command'] = disconnect
    else:
        messagebox.showwarning("連線失敗", err)

def disconnect():
    ser.close()
    com_connect['text'] = "連線"
    com_connect['command'] = connect

def address_set():
    try:
        I2C_address = int(address_text.get())
        if(I2C_address >= 12  or  I2C_address < 0):
            messagebox.showerror("數值錯誤", "位址必須為1~12")
        else:
            write_string = "02 " + "{:0>2d}".format(I2C_address) + "M"
            if ser.is_open :
                ser.write(write_string.encode("UTF-8"))
            else:
                messagebox.showwarning("請先連線", "請先連線")
    except Exception as E:
        messagebox.showerror("數值錯誤", E)
    print(I2C_address)


def address_get():
    if ser.is_open :
        try:
            ser.reset_input_buffer()
            ser.write("03M".encode("UTF-8"))
            time.sleep(0.008)
            receive = ser.read_until('M')[0:2]
            messagebox.showinfo("當下位址", receive)
        except Exception as E:
            messagebox.showerror("錯誤", E)

def change(num):
    ver_servo = vertical_servo_gui.get() + 1500
    hor_servo = horizon_servo_gui.get() + 1500
    trans_data = "06 " + "{:0>4d}".format(hor_servo) + " " + "{:0>4d}".format(ver_servo) + "M"
    if(ser.is_open):
        try:
            ser.write(trans_data.encode("UTF-8"))
        except Exception as E:
            messagebox.showerror('Error', E)
    ###vertical_servo_gui.set(0)
    ###horizon_servo_gui.set(0)

def set_horizon_0():
    if(ser.is_open):
        try:
            ser.write("04M".encode("UTF-8"))
            horizon_servo_gui.set(0)
        except Exception as E:
            messagebox.showerror("error", E)
    else:
        messagebox.showwarning("沒有連線", "請先連線")

def set_vertical_0():
    if(ser.is_open):
        try:
            ser.write("05M".encode("UTF-8"))
            vertical_servo_gui.set(0)
        except Exception as E:
            messagebox.showerror("error", E)
    else:
        messagebox.showwarning("沒有連線", "請先連線")

    

root = tk.Tk()
root.title("投射燈調整程式")
root.resizable(False, False)
root.geometry('600x600')
root.iconbitmap(self_path + "Python\\logo.ico")



Top_frame = tk.Frame(root, bd=2, relief="raise")
Top_frame.pack(side = "top", fill="x")
port_refresh()
#### port selecter
port_label = ttk.Label(Top_frame, text="序列埠:").pack(side='left')
port_GUI = tk.StringVar()
port_GUI.set("請選擇序列埠")
port_menu = tk.OptionMenu(Top_frame, port_GUI, *com_list_description)
port_menu.pack(side="left")
#### refresh Button
com_refresh = ttk.Button(Top_frame, text="重新整理", command=port_refresh)        
com_refresh.pack(side="left")
#### port connect
com_connect = ttk.Button(Top_frame, text="連線", command=connect)        
com_connect.pack(side="left")

address_Frame = tk.Frame(root, bd=2, relief="raise")
address_Frame.pack(side="top", fill="x")
address_label = tk.Label(address_Frame, text="位址:")
address_label.pack(side="left")
address_text = tk.Entry(address_Frame, width=5)
address_text.pack(side="left")
address_set_but = ttk.Button(address_Frame, text="設定", command=address_set)
address_set_but.pack(side="left")
address_read_but = ttk.Button(address_Frame, text="當下位址查詢", command=address_get)
address_read_but.pack(side="left")
servo_hor_set0 = ttk.Button(address_Frame, text="設定水平伺服機為中心點", command=set_horizon_0)
servo_hor_set0.pack(side="left")
servo_ver_set0 = ttk.Button(address_Frame, text="設定垂直伺服機為中心點", command=set_vertical_0)
servo_ver_set0.pack(side="left")


servo_GUI = tk.Frame(root)
servo_GUI.pack(side="top")
vertical_servo = tk.IntVar()
horizon_servo =  tk.IntVar()
vertical_servo_gui = tk.Scale(servo_GUI, length=500, variable=vertical_servo, orient='vertical', from_=-400, to=400, width=15, resolution=1, command=change, label="vertical")
vertical_servo_gui.pack(side="left")
horizon_servo_gui = tk.Scale(servo_GUI, length=500, variable=horizon_servo, orient='vertical', from_=-400, to=400, width=15, resolution=1, command=change, label="horizon")
horizon_servo_gui.pack(side="left")#### servo_adj


run = 1
loop_()
root.mainloop()

try:
    ser.close()
except:
    pass
