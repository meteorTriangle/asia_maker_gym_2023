import json
import numpy

class convert:
    def __init__(self, file_path):
        self.path = file_path
        self.str = ""
        self.json = None
        self.name = ["light1", "light2", "light3"]
        self.data = {
            self.name[0]:[],
            self.name[1]:[],
            self.name[2]:[]
            }
        self.data2 = {
            self.name[0]:{"time": [], "degree":[[],[]]},
            self.name[1]:{"time": [], "degree":[[],[]]},
            self.name[2]:{"time": [], "degree":[[],[]]}
            }

    def convert(self):
        self.data2[self.name[0]]["time"] = []
        self.data2[self.name[0]]["degree"][0] = []
        self.data2[self.name[0]]["degree"][1] = []
        try:
            self.str = open(self.path)
        except Exception as E:
            return "路徑錯誤"
        try:
            self.json = json.load(self.str)
        except Exception as E:
            return "格式錯誤"
        for j in range(3):
            Ll1 = self.json[self.name[j]]
            for i in range(len(Ll1)):
                Lz2 = {"time": 0, "degree": [0, 0]}
                time_str = Ll1[i]["time"]
                time_f = int(time_str[0:1])*60 + float(time_str[3:7])
                print(time_f)
                Lz2["time"] = time_f
                Lz2["degree"] = Ll1[i]["degree"]
                self.data[self.name[j]].append(Lz2)
                self.data2[self.name[j]]["time"].append(time_f)
                self.data2[self.name[j]]["degree"][0].append(int(Ll1[i]["degree"][0]))
                self.data2[self.name[j]]["degree"][1].append(int(Ll1[i]["degree"][1]))
        print(self.data2)
        return False
    
    def run(self, time_ms):
        vaa = [[0,0], [0,0], [0,0]]
        for j in range(3):
            ls1 = self.data2[self.name[j]]
            vaa[j][0] = numpy.interp(time_ms/1000, ls1["time"], ls1["degree"][0], left=0)
            vaa[j][1] = numpy.interp(time_ms/1000, ls1["time"], ls1["degree"][1], left=0)
        return vaa