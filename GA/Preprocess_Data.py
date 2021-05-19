import numpy
import os
import Config
class Data:

    def __init__(self):
        self.linkdata = os.path.join(Config.LINK_FORDER,Config.DATA_FILE)
    
    def read_data(self):
        data = open(self.linkdata)
        lines = data.readlines()
        count = 0
        data1 = {}
        line_data_raw = lines[0].split(" ")
        data1["N"] = int(line_data_raw[0])
        data1["A"] = int(line_data_raw[1])
        data1["C"] = int(line_data_raw[2])
        data1["c"] = list(map(int, lines[1].split(" ")))
        data1["a"] = list(map(int, lines[2].split(" ")))
        data1["f"] = list(map(int, lines[3].split(" ")))
        data1["m"] = list(map(int, lines[4].split(" ")))
        return data1