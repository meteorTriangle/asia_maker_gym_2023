import tkinter as tk
from tkinter import ttk
from tkinter.constants import *
from tkinter import messagebox
from tkinter import font as tkf
from GUI.Top_ports import port_frames as PF
import queue


global q
def queue_set(q_):
    global q
    q = q_

def GUI():
    global q
    root = windows()
    PF.port_frame(root, q)
    root.mainloop()
    for i in range(10):
        q['STOP'].put("stop")




def windows():
    root = tk.Tk()
    root.title('servo adjust')
    root.resizable(False, False)
    root.geometry('1280x720')
    return root  