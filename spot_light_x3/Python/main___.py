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

### import threading as th
### import queue
#### sub
import serial__.ser as sser
self_path = os.path.dirname(__file__) + "\\"
##self_path = ""
servo_change = False
elevator_in_change = False
run = 1
LED_change = False

###pyserial
BAUD_RATES = 10000000

single_servo_frame = list(range(9))
horizon_servo_gui = list(range(9))
vertical_servo_gui = list(range(9))
vertical_servo = list(range(9))
horizon_servo = list(range(9))
LED_frame = list(range(9))
LED_butt = list(range(9))

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
root.geometry('1580x950')
root.iconbitmap(self_path + "Python\\logo.ico")

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

def loop_():
    now_time = sj.get_time()
    sec_I = (now_time % 600000) / 1000
    min_I = now_time // (60*1000)
    sec_I = sec_I - (min_I*60)
    min_S = "{:0>2d}".format(int(min_I))
    sec_S = '%05.2f' % sec_I
    time_text=  min_S + ":" + sec_S
    timer_label["text"]=time_text
    if(sj.timer_state):
        if(sj.pause_state == False):
            servo_data = sj.run_json()
            if type(servo_data) is str:
                messagebox.showinfo("錯誤", servo_data)
            else:
                for j in range(12):
                    horizon_servo_gui[j].set(servo_data[j][0])
                    vertical_servo_gui[j].set(servo_data[j][1])
    global servo_change
    if(com_connect['text'] == "斷線" and servo_change):
        trans_data = '04'
        transdata_time_ = sj.get_R_time()
        
        for j in range(9):
            trans_data = trans_data + "{:0>4X}".format(int(horizon_servo_gui[j].get()*2000/180 + 500))
            trans_data = trans_data + "{:0>4X}".format(int(vertical_servo_gui[j].get()*2000/180 +500))
        
        
        error_state = sj.transport(bytes.fromhex(trans_data))
        ###error_state = sj.transport(bytes.fromhex("0102000000"))
        transdata_time = int(sj.get_R_time() - transdata_time_)
        delay_display["text"] = str(transdata_time)
        print(bytes.fromhex(trans_data))
        print((trans_data))
        if error_state is True:
            messagebox.showinfo("斷線", sj.error)
            com_connect['text'] = "連線"
            sj.disconnect()
        servo_change = False
    time.sleep(0.01)
    if(com_connect['text'] == "斷線"):
        trans_data = '05'
        for j in range(9):
            tk.Button()
            trans_data = trans_data + ("FF","00")[LED_butt[j]["red"]["bg"] == "#FFFFFF"]
            trans_data = trans_data + ("FF","00")[LED_butt[j]["green"]["bg"] == "#FFFFFF"]
            trans_data = trans_data + ("FF","00")[LED_butt[j]["blue"]["bg"] == "#FFFFFF"]
        error_state = sj.transport(bytes.fromhex(trans_data))
        ##print(bytes.fromhex(trans_data))
        ##print((trans_data))
        if error_state is True:
            messagebox.showinfo("斷線", sj.error)
            com_connect['text'] = "連線"
            sj.disconnect()
    time.sleep(0.01)
    if(com_connect['text'] == "斷線" and elevator_in_change):
        trans_data = '06'
        trans_data = trans_data + "{:0>4X}".format(int(elevator_servo_gui.get()*2000/180 + 500))
        error_state = sj.transport(bytes.fromhex(trans_data))
        if error_state is True:
            messagebox.showinfo("斷線", sj.error)
            com_connect['text'] = "連線"
            sj.disconnect()
    root.after(30, loop_)

def play_C():
    if(sj.timer_state):
        pass
    else:
        sj.file_path = file_path
        sj.pause_state = False
        sj.timer_state = True
        sj.timer_reset()
        play_button["bg"] = "gray"

def stop_C():
    sj.timer_state = False
    pause_button["bg"] = "white"
    play_button["bg"] = "white"

def pause_C():
    if(sj.timer_state):
        if(sj.pause_state):
            sj.timer_resume()
            pause_button["bg"] = "white"
            play_button["bg"] = "gray"
        else:
            sj.timer_pause()
            pause_button["bg"] = "gray"
            play_button["bg"] = "white"

def fastT_C():
    if sj.timer_state :
        sj.timerPause = sj.timerPause + 5000

def backT_C():
    if sj.timer_state :
        if(sj.get_time() <= 5000):
            sj.timer_reset()
        else:
            sj.timerPause = sj.timerPause - 5000
            
def chaange(num):
    global servo_change
    servo_change = True
def elevator_change(num):
    global elevator_in_change
    elevator_in_change = True

img = Image.open(self_path + "Python\\LOGO.png")
img = img.resize((96, 38))
tk_img = ImageTk.PhotoImage(img)


BBfont = tkf.Font(size=19)

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
### time
delay_display = tk.Label(Top_frame, text="0")
delay_display.pack(side="left")

Lfont = tkf.Font(size=30)

#### scale block
setting_frame = tk.Frame(root, width=1280, height=470)                  ### servo frame
setting_frame.pack(side="top")


for i in range(9):
    single_servo_frame[i] = tk.Frame(setting_frame, bd=5, relief='groove')
    single_servo_frame[i].grid(column=i, row=0)
    LED_frame[i] = tk.Frame(single_servo_frame[i])
    LED_frame[i].pack(side='bottom')
    tittle = tk.Label(single_servo_frame[i], text='Light'+str(i+1), font=Lfont)
    tittle.pack()
    vertical_servo[i] = tk.DoubleVar()
    horizon_servo[i] = tk.DoubleVar()
    vertical_servo_gui[i] = tk.Scale(single_servo_frame[i], 
                                     length=370, 
                                     variable=vertical_servo[i], 
                                     orient='vertical', 
                                     from_=0, to=180, 
                                     width=15, 
                                     resolution=0.1, 
                                     command=chaange)
    vertical_servo_gui[i].pack(side="left")
    horizon_servo_gui[i] = tk.Scale(single_servo_frame[i], length=370, variable=horizon_servo[i], orient='vertical', from_=0, to=180, width=15, resolution=0.1, command=chaange)
    horizon_servo_gui[i].pack(side="left")
    c = i
    LED_butt[i] = {
        "red": tk.Button(LED_frame[i], 
                         height=1, 
                         width=1, 
                         background="#FF0000", 
                         activebackground="#FFFFFF", 
                         command=lambda n=i: LED_butt[n]["red"].config(bg=(("#FF0000", "#FFFFFF")[LED_butt[n]["red"]["bg"]=="#FF0000"]))),
        "green": tk.Button(LED_frame[i], 
                           height=1, 
                           width=1, 
                           background="#00FF00", 
                           activebackground="#FFFFFF", 
                           command=lambda n=i: LED_butt[n]["green"].config(bg=(("#00FF00", "#FFFFFF")[LED_butt[n]["green"]["bg"]=="#00FF00"]))),
        "blue": tk.Button(LED_frame[i], 
                          height=1, 
                          width=1, 
                          background="#0000FF", 
                          activebackground="#FFFFFF", 
                          command=lambda n=i: LED_butt[n]["blue"].config(bg=(("#0000FF", "#FFFFFF")[LED_butt[n]["blue"]["bg"]=="#0000FF"])))
    }
    LED_butt[i]["red"].grid(column=0, row=0)
    LED_butt[i]["green"].grid(column=1, row=0)
    LED_butt[i]["blue"].grid(column=2, row=0)
elevator_frame = tk.Frame(setting_frame, bd=5, relief="groove", height=500)
elevator_frame.grid(column=10, row=0)
tittle = tk.Label(elevator_frame, text='Elevator', font=Lfont)
tittle.pack()
elevator_servo_var = tk.DoubleVar()
elevator_servo_gui = tk.Scale(elevator_frame, length=370, variable=elevator_servo_var, orient='vertical', from_=0, to=180, width=15, resolution=0.1, command=elevator_change)
elevator_servo_gui.pack(side="left")
    

but_frame = tk.Frame(root)
but_frame.pack(fill="both")
### play option
play_frame = tk.Frame(but_frame, bd=2, relief='groove')
play_frame.pack(side="top", fill="x")
### load icon
play_img = Image.open(self_path + "Python\\icon\\play-button-arrowhead.png")
play_img = play_img.resize((30, 30))
play_tk_img = ImageTk.PhotoImage(play_img)

pause_img = Image.open(self_path + "Python\\icon\\pause.png")
pause_img = pause_img.resize((30, 30))
pause_tk_img = ImageTk.PhotoImage(pause_img)

stop_img = Image.open(self_path + "Python\\icon\\stop-button.png")
stop_img = stop_img.resize((30, 30))
stop_tk_img = ImageTk.PhotoImage(stop_img)

fast_img = Image.open(self_path + "Python\\icon\\fast-forward.png")
fast_img = fast_img.resize((30, 30))
fast_tk_img = ImageTk.PhotoImage(fast_img)

back_img = Image.open(self_path + "Python\\icon\\rewind-button.png")
back_img = back_img.resize((30, 30))
back_tk_img = ImageTk.PhotoImage(back_img)

### font
timer_font = tkf.Font(size=24)

### button
play_button = tk.Button(play_frame, image=play_tk_img, command=play_C, bg="white")
play_button.pack(side="left")
pause_button = tk.Button(play_frame, image=pause_tk_img, command=pause_C, bg="white")
pause_button.pack(side="left")
stop_button = tk.Button(play_frame, image=stop_tk_img, command=stop_C, bg="white")
stop_button.pack(side="left")
back_button = tk.Button(play_frame, image=back_tk_img, bg="white", command=backT_C)
back_button.pack(side="left")
fast_button = tk.Button(play_frame, image=fast_tk_img, bg="white", command=fastT_C)
fast_button.pack(side="left")
timer_label = tk.Label(play_frame, text="00:00.00", font=timer_font, bd=1, relief='raise')
timer_label.pack(side="left")

#### text editor
txt = scrolledtext.ScrolledText(but_frame, height=500, width=230)
txt.pack()



port_refresh()

###window.iconbitmap('icon.ico')
run = 1
loop_()
root.mainloop()
sj.timer_state=False

try:
    sj.disconnect()
except:
    pass

# 