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
                Function_1(receive)
            if(function_SN==2):
                Function_2(receive)
    
        time.sleep(0.002)
        if(q["STOP"].empty()==False):
            non_stop = False
            



def function_set(receive):
    function = 0
    if(receive["Function"]=="read com list"):
        function = 1
        return(function)
    if(receive["Function"]=="connect"):
        function = 2
        return function

def Function_1(receive):
    global ser
    global q
    com_list = serial.tools.list_ports_windows.comports()
    com_description = []
    com_name = []
    for p in com_list:
        com_description.append(p.description)
        com_name.append(p.name)
    tr = {
        "command SN": 1,
        "com description": com_description,
        "com name": com_name
    }
    q['STG'].put(tr)

def Function_2(receive):
    global ser
    global q
    excep = ""
    success = False
    try:
        ser = serial.Serial(receive["com_name"], receive["BAUD_RATE"])
        success = True
    except Exception as ee:
        excep = ee
        print(ee)
    tr = {"command SN": 2,
           "Success": success,
           "exception":excep
           }
    q['STG'].put(tr)
    