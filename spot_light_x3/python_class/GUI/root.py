import tkinter as tk
from tkinter import ttk
from tkinter.constants import *
from tkinter import messagebox
from tkinter import font as tkf
import serial 

class window:
    ##root = None
    def __init__(self, title):
        self.title = title
    
    def create(self):
        self.tk = tk.Tk()
        self.tk.title(self.title)
        self.tk.resizable(False, False)
        self.tk.iconbitmap('python_class\GUI\logo.ico')
        self.tk.geometry('1280x720')
    def run(self):
        self.tk.mainloop()

class ser__:
    def __init__(self, BAUD_RATE, COM_NAME):
        self.com = COM_NAME
        self.baub = BAUD_RATE
    def connect(self):
        try:
            self.ser = serial.Serial(self.com, self.baub)
            return(True)
        except Exception as error:
            self.error = error
            print(self.error)
            return False
    def error_get(self):
        return self.error

class option_menu:
    def __init__(self, frame_, option_, default_text, list_):
        self.frame_ = frame_
        self.option_ = option_
        self.def_text = default_text
        self.list = list_
    def create(self):
        self.tk_op = tk.StringVar()
        self.tk_op.set(self.option_)
        if(len(self.list) == 0):
            self.list.append(self.def_text)
        self.tk = tk.OptionMenu(self.frame_, self.tk_op, *self.list)
        return self.tk
    def change_op(self, new_op):
        self.option_ = new_op
        self.tk['menu'].delete(0, 'end')
        for i in self.option_:
            self.tk['menu'].add_command(label=i, command=tk._setit(self.tk_op, i))
