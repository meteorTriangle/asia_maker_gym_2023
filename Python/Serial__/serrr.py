import queue 
import serial
import serial.tools.list_ports_windows
import time

ser = None
q = None
baudrate = 115200

def inti_ser(baudrate_, q_):
    global baudrate
    global q
    baudrate = baudrate_
    q = q_

def Ser_loop():
    global baudrate
    global q
    non_stop = True
    while(non_stop) :
        if(q['GTS'].empty()==False):
            receive = q['GTS'].get()
            function_SN = function_set(receive)
            if(function_SN==1):
                global ser
                com_list = serial.tools.list_ports_windows.comports()
                com_description = []
                for p in com_list:
                    com_description.append(p.description)
                q['STG'].put(com_description)
    


        time.sleep(0.002)
        if(q["STOP"].empty()==False):
            non_stop = False
            



def function_set(receive):
    function = 0
    ## string
    if(isinstance(receive, str)):
        if(receive=="read com list"):
            function = 1
            return(function)

    