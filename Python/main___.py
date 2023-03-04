#### Serial
import serial
import serial.tools.list_ports_windows
#### GUI
import tkinter as tk
from tkinter import ttk
from tkinter.constants import *
from tkinter import messagebox
from tkinter import font as tkf
from PIL import Image, ImageTk
import time
#### sub

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

## GUI run
root = tk.Tk()
root.title('servo adjust')
root.resizable(False, False)
root.geometry('1280x720')
root.iconbitmap("Python\logo.ico")

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
    try:
        global ser
        ser = serial.Serial(com_list_name[COM_PORT_index], BAUD_RATES)
        messagebox.showinfo("連線成功", "連線成功")
        com_connect['text'] = "斷線"
        com_connect['command'] = disconnect
        print(str(ser.isOpen()))
    except Exception as e:
        messagebox.showinfo("連線失敗", e)
    
def disconnect():
    global ser
    ser.close()
    com_connect['text'] = "連線"
    com_connect['command'] = connect

def transport(nummm):
    global ser
    global horizon_servo_gui
    global ms
    noError = 1
    try:
        ser.isOpen()
    except:
        messagebox.showinfo("Error", '請先連線')
        noError = 0

    if noError:
        if int(time.time()*1000) > ms+20 :
            trans_data = ''
            for j in range(3):
                print(str(horizon_servo_gui[j].get()).zfill(3))
                print(str(vertical_servo_gui[j].get()).zfill(3))
                trans_data = trans_data + str(horizon_servo_gui[j].get()).zfill(3) + " "
                trans_data = trans_data + str(vertical_servo_gui[j].get()).zfill(3) + " "
            trans_data = '121m' + trans_data[0:23]+'M'
            ser.write(trans_data.encode('UTF-8'))
            print(trans_data.encode('ASCII'))
            ms = int(time.time()*1000)
            ser.flushInput()
    
        
        


## Top frame(port setting)
Top_frame = ttk.Frame(root)
Top_frame.pack(side = "top", fill="x")

## port selecter
port_label = ttk.Label(Top_frame, text="序列埠:").pack(side='left')              
port_GUI = tk.StringVar()
port_GUI.set("請選擇序列埠")
port_menu = tk.OptionMenu(Top_frame, port_GUI, *com_list_description)
port_menu.pack(side="left")
## refresh Button
com_refresh = ttk.Button(Top_frame, text="重新整理", command=port_refresh)        
com_refresh.pack(side="left")
#### port connect
com_connect = ttk.Button(Top_frame, text="連線", command=connect)        
com_connect.pack(side="left")
### logo
img = Image.open("Python\LOGO.png")
img = img.resize((96, 38))
tk_img = ImageTk.PhotoImage(img)
Logo = tk.Label(Top_frame, image=tk_img, height=38, width=96)
Logo.pack(side="left")

Lfont = tkf.Font(size=30)

#### scale block
setting_frame = tk.Frame(root, width=1280, height=320)                  ### servo frame
setting_frame.pack(side="top")


for i in range(3):
    single_servo_frame[i] = tk.Frame(setting_frame, bd=5, relief='groove')
    single_servo_frame[i].grid(column=i, row=0)
    tittle = tk.Label(single_servo_frame[i], text='Light'+str(i), font=Lfont)
    tittle.pack()
    vertical_servo[i] = tk.IntVar()
    horizon_servo[i] = tk.IntVar()
    vertical_servo_gui[i] = tk.Scale(single_servo_frame[i], length=200, variable=vertical_servo[i], orient='vertical', from_=0, to=90, width=30, command=transport, resolution=1)
    vertical_servo_gui[i].pack()
    horizon_servo_gui[i] = tk.Scale(single_servo_frame[i], length=400, variable=horizon_servo[i], orient='horizon', from_=0, to=180,width=30, command=transport, resolution=1)
    horizon_servo_gui[i].pack()


#### tracks
track_lengh = 5000
track_f = tk.Frame(root, bd=5, relief='groove') 
track_f.pack()
tool_frame = tk.Frame(track_f, bd=1, relief="groove", width=25)
tool_frame.pack(side="left", fill="y")
scale = tk.Canvas(track_f, width=track_lengh, height=20, relief='groove', bd=2)
track = tk.Canvas(track_f, width=track_lengh, height=500, relief='groove', bd=2)
xsb = tk.Scrollbar(track_f, orient="horizontal", command=track.xview)
ysb = tk.Scrollbar(track_f, orient="vertical", command=track.yview)
xsb.pack(side="bottom", fill="x")
ysb.pack(side="right", fill="y")
scale.pack()
track.pack()


port_refresh()

###window.iconbitmap('icon.ico')
run = 1

root.mainloop()

try:
    ser.close()
except:
    pass

# 