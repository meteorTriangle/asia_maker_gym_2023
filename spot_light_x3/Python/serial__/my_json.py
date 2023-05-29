import json
import numpy

class convert:
    def __init__(self, file_path):
        self.path = file_path
        self.str = ""
        self.json = None
        self.data = {
            "light1":[],
            "light2":[],
            "light3":[],
            "light4":[],
            "light5":[],
            "light6":[],
            "light7":[],
            "light8":[],
            "light9":[],
            "elevator":[]
            }

    def convert(self):
        self.data.clear()
        self.data = {
            "light1":[],
            "light2":[],
            "light3":[],
            "light4":[],
            "light5":[],
            "light6":[],
            "light7":[],
            "light8":[],
            "light9":[],
            "elevator":[]
            }
        try:
            self.str = open(self.path)
        except Exception as E:
            return "路徑錯誤"
        try:
            self.json = json.load(self.str)
        except Exception as E:
            return "格式錯誤"
        
        ##default 
        for i in range(10):
            key_name = list(self.json["default"].keys())[i]
            self.data[key_name].append({"00:00.00": self.json["default"][key_name]})

    
        for action_data in self.json["action"]:
            time = action_data["time"]
            for device_name in list(action_data.keys()):
                if device_name == "time":
                    pass
                else:
                    self.data[device_name].append({time: action_data[device_name]})
        for i in range(9):
            single_device_data = self.data[list(self.data.keys())[i]]
            single_device_data_con = {"servo_H": {"time": [], "deg": []}, 
                                      "servo_V": {"time": [], "deg": []},
                                      "LED": {"time": [], "led": []}}
            for frame in single_device_data:
                dataa = frame[list(frame.keys())[0]]
                time_str = list(frame.keys())[0]
                time_f = int(time_str[0:1])*60 + float(time_str[3:7])
                if(dataa[0] != -1):
                    single_device_data_con["servo_H"]["time"].append(time_f)
                    single_device_data_con["servo_H"]["deg"].append(dataa[0])
                if(dataa[1] != -1):
                    single_device_data_con["servo_V"]["time"].append(time_f)
                    single_device_data_con["servo_V"]["deg"].append(dataa[1])
                single_device_data_con["LED"]["time"].append(time_f)
                single_device_data_con["LED"]["led"].append(dataa[2:5])
            self.data[list(self.data.keys())[i]] = single_device_data_con
        return False
    
    def run(self, time_ms):
        vaa = []
        for j in range(9):
            ls1 = []
            ls1.append(numpy.interp(time_ms/1000, self.data[list(self.data.keys())[j]]["servo_H"]["time"], self.data[list(self.data.keys())[j]]["servo_H"]["deg"], left=0))
            ls1.append(numpy.interp(time_ms/1000, self.data[list(self.data.keys())[j]]["servo_V"]["time"], self.data[list(self.data.keys())[j]]["servo_V"]["deg"], left=0))
            time_s = time_ms/1000
            st = True
            cti = 0 
            if(len(self.data[list(self.data.keys())[j]]["LED"]["time"]) == 1):
                LED_lst = self.data[list(self.data.keys())[j]]["LED"]["led"][0]
                pass
            else:
                while st:
                    st = self.data[list(self.data.keys())[j]]["LED"]["time"][cti] <= time_s 
                    LED_lst = self.data[list(self.data.keys())[j]]["LED"]["led"][cti]
                    cti+=1
                    if(len(self.data[list(self.data.keys())[j]]["LED"]["time"]) == cti):
                        st = False
            ls1.append(LED_lst)
            vaa.append(ls1)
        print(vaa)
        return vaa