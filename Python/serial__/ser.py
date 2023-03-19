import serial
import serial.tools.list_ports_windows
import time
import serial__.my_json as my_json


class serial_json:
    def __init__(self, baudrates):
        self.port_list = serial.tools.list_ports_windows.comports()
        self.com_port = None
        self.error = ""
        self.BAUD_RATE = baudrates
        self.ser = None
        self.file_path = None
        self.timer = 0
        self.refTime = time.time_ns()
        self.timer_state=False
        self.timerPause = 0
        self.pause_state = False
        self.jj = my_json.convert(self.file_path)
        self.err = ""

    def port_refresh(self):
        self.port_list = serial.tools.list_ports_windows.comports()
        return self.port_list
    
    def connect(self, com):
        self.com_port = com
        try:
            self.ser = serial.Serial(self.com_port, self.BAUD_RATE)
            return False
        except Exception as error:
            self.error = error
            return True

    def disconnect(self):
        self.ser.close()

    def transport(self, data):
        try:
            self.ser.write(data)
            return False
        except Exception as s:
            self.error = "請先連線"
            return True
        
    def run_json(self):
        servo = self.jj.run(self.get_time())
        return servo

    def get_time(self):
        self.timer = (time.time_ns() - self.refTime) / 1000000
        if (self.timer_state):
            if(self.pause_state):
                return self.timerPause
            else:
                return (self.timer + self.timerPause)
        else:
            return 0
        
    def timer_reset(self):
        self.refTime = time.time_ns()
        self.timerPause = 0
        self.jj.path = self.file_path
        self.err = self.jj.convert()
        print(self.err)


    def timer_pause(self):
        self.timerPause = self.get_time()
        self.pause_state = True
    
    def timer_resume(self):
        self.jj.path = self.file_path
        self.err = self.jj.convert()
        self.refTime = time.time_ns()
        self.pause_state = False


