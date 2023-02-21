#### Serial
import serial
import serial.tools.list_ports_windows
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
q_list_g = {'STG':STG, 'GTS':GTS}
GUI.queue_set(q_list_g)

## TH
GUI_th = th.Thread(target = GUI.GUI)