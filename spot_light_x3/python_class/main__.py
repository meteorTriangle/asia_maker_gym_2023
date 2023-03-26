import GUI.root as GUI
import tkinter as tk

Icon = None
windows = GUI.window("Servo adjuster")
windows.create()
ser = GUI.ser__(1, 1)

Top_frame = tk.Frame(windows.tk)
Top_frame.pack(side="top", fill="x")

port_op = GUI.option_menu(Top_frame, )

































windows.run()