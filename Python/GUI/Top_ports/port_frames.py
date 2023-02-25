import tkinter as tk
from tkinter import ttk
from tkinter.constants import *
from tkinter import messagebox
from tkinter import font as tkf
import queue

global q
global port_menu
global port_GUI

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
    print(com_list_description)
    global port_menu
    port_menu = tk.OptionMenu(Top_frame, port_GUI, *com_list_description)
    port_menu.pack(side="left")
    #### refresh Button
    refresh_But = ttk.Button(Top_frame, text="重新整理", command=port_refresh)        ##, command=port_refresh
    refresh_But.pack(side="left")
    #### port connect
    com_connect = ttk.Button(Top_frame, text="連線")         ##, command=connect
    com_connect.pack(side="left")
    return Top_frame

def read_com_list(q_):
    q_['GTS'].put('read com list')
    while(q_['STG'].empty()):
        pass
    list = q_["STG"].get()
    return list

def port_refresh():
    global port_menu
    global q
    global port_GUI
    new_com_list =  read_com_list(q)
    port_menu['menu'].delete(0, 'end')
    for i in new_com_list:
        port_menu['menu'].add_command(label=i, command=tk._setit(port_GUI, i))
