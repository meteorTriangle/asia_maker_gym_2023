import serial
import serial.tools.list_ports_windows


class serial_json:
    def __init__(self, baudrates):
        self.port_list = serial.tools.list_ports_windows.comports()
        self.com_port = None
        self.error = ""
        self.BAUD_RATE = baudrates
        self.ser = None
        self.file_path= None

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
        
    def run_json(self, file_path):
        self.file_path = file_path
        




