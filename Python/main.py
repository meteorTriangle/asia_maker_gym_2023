#### Serial
import Serial__.serrr as sser
#### GUI
import tkinter as tk
from tkinter import ttk
from tkinter.constants import *
from tkinter import messagebox
from tkinter import font as tkf
import time
#### thread
import threading as th
import queue
#### sub
from GUI import GUI


###serial setting
BAUD_RATES = 115200

## queue
STG = queue.Queue(maxsize=30)
GTS = queue.Queue(maxsize=30)
stop = queue.Queue(maxsize=30)
q_list_g = {'STG':STG, 'GTS':GTS, 'STOP':stop}
GUI.queue_set(q_list_g)

## ser
sser.inti_ser(BAUD_RATES, q_list_g)

## TH
GUI_th = th.Thread(target = GUI.GUI)
SER_th = th.Thread(target = sser.Ser_loop)
GUI_th.start()
SER_th.start()


###while(GUI_th.is_alive()):
###    pass
  
