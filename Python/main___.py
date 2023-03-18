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
import ctypes
import sys

import threading as th
import queue
import time
#### sub
import serial__.ser as sser

run = 1

###pyserial
BAUD_RATES = 115200
ser = None

ms = int(time.time()*1000)

single_servo_frame = list(range(3))
horizon_servo_gui = list(range(3))
vertical_servo_gui = list(range(3))
vertical_servo = list(range(3))
horizon_servo = list(range(3))

vertical_servo_id = id(vertical_servo)
horizon_servo_id = id(horizon_servo)

com_list_description = ['']
com_list_name = []

file_path = "Untitle"
fileTypes = [("JSON","*.json")]

## GUI run
root = tk.Tk()
root.title(file_path)
root.resizable(False, False)
root.geometry('1280x950')
root.iconbitmap("Python\logo.ico")

sj = sser.serial_json(BAUD_RATES)


def port_refresh():
    ### com port read
    com_list_description.clear()
    com_list_name.clear()
    ports = sj.port_refresh()
    for p in ports:
        com_list_description.append(p.description)
        com_list_name.append(p.name)
        print(p.description)
        print(p.name)
    print(len(ports), 'ports found')
    
    ###
    if len(ports) == 0:
        messagebox.showinfo("Error", "請插入Arduino")
    if run == 1:
        port_menu['menu'].delete(0, 'end')

        for i in com_list_description:
            port_menu['menu'].add_command(label=i, command=tk._setit(port_GUI, i))

def connect():
    COM_PORT = port_GUI.get()
    if COM_PORT == '請選擇序列埠':
        messagebox.showinfo("Error", '請選擇序列埠')
    else:
        COM_PORT_index = com_list_description.index(COM_PORT)
        print(com_list_name[COM_PORT_index])
    err_state = sj.connect(com_list_name[COM_PORT_index])
    if(err_state == False):
        messagebox.showinfo("連線成功", "連線成功")
        com_connect['text'] = "斷線"
        com_connect['command'] = disconnect
    else:
        messagebox.showinfo("連線失敗", sj.error)
    
def disconnect():
    sj.disconnect()
    com_connect['text'] = "連線"
    com_connect['command'] = connect

def transport(nummm):
    global ser
    global horizon_servo_gui
    global ms
    noError = 1

    trans_data = ''
    for j in range(3):
        print(str(horizon_servo_gui[j].get()).zfill(3))
        print(str(vertical_servo_gui[j].get()).zfill(3))
        trans_data = trans_data + str(horizon_servo_gui[j].get()).zfill(3) + " "
        trans_data = trans_data + str(vertical_servo_gui[j].get()).zfill(3) + " "
    trans_data = '121m' + trans_data[0:23]+'M'
    error_state = sj.transport(trans_data.encode('UTF-8'))
    if(error_state):
        messagebox.showinfo("連線失敗", sj.error)
    

def open__file():
    global file_path
    file_path = filedialog.askopenfilename(filetypes = fileTypes)
    with open(file_path, 'r') as f:
        txt.delete(1.0,END)
        txt.insert(INSERT,f.read())
    root.title(file_path)
    
def save__file(save_as):
    global file_path
    if(file_path == "Untitle" or save_as == True):
        file_path = filedialog.asksaveasfilename(filetypes = fileTypes)
        file_path = file_path + ".json"
    with open(file_path, 'w') as f:
        f.write(txt.get('1.0','end'))
    root.title(file_path)

def save__():
    save__file(False)

def save__as():
    save__file(True)


img = Image.open("Python\LOGO.png")
img = img.resize((96, 38))
tk_img = ImageTk.PhotoImage(img)


BBfont = tkf.Font(size=19)
"""
## function selection block
top_function_frame = tk.Frame(root, height=38, bd=2, relief="raised")  ###, bd=2, relief="raised"
top_function_frame.pack(fill="x")
function_port = tk.Button(top_function_frame, text="PORT", width=7, font=BBfont)
function_port.pack(side="left")
function_scale = tk.Button(top_function_frame, text="SCALE", width=7, font=BBfont)
function_scale.pack(side="left")
function_ig = tk.Button(top_function_frame, image=tk_img)
function_ig.pack(side="right")
"""


## Top frame(port setting)
Top_frame = ttk.Frame(root)
Top_frame.pack(side = "top", fill="x")

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
#### open file
open_file_but = ttk.Button(Top_frame, text="開啟檔案", command=open__file)
open_file_but.pack(side="left")
#### save file
save_file_but = ttk.Button(Top_frame, text="儲存檔案", command=save__)
save_file_but.pack(side="left")
#### save as file
save_as_file_but = ttk.Button(Top_frame, text="另存新檔", command=save__as)
save_as_file_but.pack(side="left")
### logo
## Logo = tk.Label(Top_frame, image=tk_img, height=38, width=96)
## Logo.pack(side="left")

Lfont = tkf.Font(size=30)

#### scale block
setting_frame = tk.Frame(root, width=1280, height=400)                  ### servo frame
setting_frame.pack(side="top")


for i in range(3):
    single_servo_frame[i] = tk.Frame(setting_frame, bd=5, relief='groove')
    single_servo_frame[i].grid(column=i, row=0)
    tittle = tk.Label(single_servo_frame[i], text='Light'+str(i), font=Lfont)
    tittle.pack()
    vertical_servo[i] = tk.IntVar()
    horizon_servo[i] = tk.IntVar()
    vertical_servo_gui[i] = tk.Scale(single_servo_frame[i], length=370, variable=vertical_servo[i], orient='vertical', from_=0, to=180, width=30, command=transport, resolution=1)
    vertical_servo_gui[i].pack()
    horizon_servo_gui[i] = tk.Scale(single_servo_frame[i], length=400, variable=horizon_servo[i], orient='horizon', from_=0, to=180, width=30, command=transport, resolution=1)
    horizon_servo_gui[i].pack(side="bottom")


#### text editor
txt = scrolledtext.ScrolledText(root, height=500, width=1280)
txt.pack()





port_refresh()

###window.iconbitmap('icon.ico')
run = 1

root.mainloop()

try:
    sj.disconnect()
except:
    pass

# 