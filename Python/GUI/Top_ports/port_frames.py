import tkinter as tk
from tkinter import ttk
from tkinter.constants import *
from tkinter import messagebox
from tkinter import font as tkf
import queue

global q
global port_menu
global port_GUI
global com_INFO

def port_frame(root_frame, q_):
    #### queue setting
    global q
    q = q_
    #### Top frame(port setting)
    Top_frame = ttk.Frame(root_frame)
    Top_frame.pack(side = "top", fill="x")
    #### port selecter
    port_label = ttk.Label(Top_frame, text="序列埠:").pack(side='left')  
    global port_GUI            
    port_GUI = tk.StringVar()
    port_GUI.set("請選擇序列埠")
    com_list_description = read_com_list(q)
    if(len(com_list_description) == 0):
        com_list_description.append("")
    print(com_list_description)
    global port_menu
    port_menu = tk.OptionMenu(Top_frame, port_GUI, *com_list_description)
    port_menu.pack(side="left")
    #### refresh Button
    refresh_But = ttk.Button(Top_frame, text="重新整理", command=port_refresh)        ##, command=port_refresh
    refresh_But.pack(side="left")
    #### port connect
    com_connect = ttk.Button(Top_frame, text="連線", command=connect)         ##, command=connect
    com_connect.pack(side="left")
    return Top_frame

def read_com_list(q):
    global com_INFO
    F = {"Function":'read com list'}
    q['GTS'].put(F)
    while(q['STG'].empty()):
        pass
    com_INFO = q["STG"].get()
    com_list = com_INFO['com description']
    return com_list

def port_refresh():
    global port_menu
    global q
    global port_GUI
    new_com_list =  read_com_list(q)
    port_menu['menu'].delete(0, 'end')
    for i in new_com_list:
        port_menu['menu'].add_command(label=i, command=tk._setit(port_GUI, i))

def connect():
    global q
    global port_GUI
    global com_INFO
    select_com = port_GUI.get() 
    SN = com_INFO['com description'].index(select_com)
    com_name_List = com_INFO['com name']
    com_name = str(com_name_List[SN])
    print(com_name)
    tr = {"Function":'connect',
          "com_name":com_name,
          "BAUD_RATE":int(115200)
          }
    q['GTS'].put(tr)
    while(q['STG'].empty()):
        pass
    re = q['STG'].get()
    if(re['Success']):
        messagebox.showinfo("連線成功", '連線成功')
    else:
        messagebox.showinfo("Error", re["exception"])