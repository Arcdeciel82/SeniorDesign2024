# DataStore Python Library
# Curt Lynch
# This library allows for the storage and retreival of synchronized data signals to/from simple CSV files.

# File Layout
'''
signalname0,signalname1,signalname2,...
signalfrequency0,signalfrequency1.signalfrequency2,...

signal0data
signal1data
signal2data
...

'''

from collections import defaultdict
from pathlib import Path
from typing import List

class DataStore:
    # A container for easily accessing and storing a set of synchonized signals.
    signalData = defaultdict(List)
    signalFreq = {}

    def __init__(self, pathToDataFile:Path):
        self.path = Path(pathToDataFile)
        if self.path.is_file():
            self.load(pathToDataFile)

    def load(self, pathToDataFile:Path):
        """Load data from pathToDataFile."""
        pathToDataFile = Path(pathToDataFile)
        file = open(pathToDataFile)
        data = file.read().splitlines()
        keys = data[0].split(sep=",")
        freqs = data[1].split(sep=",")
        for name, freq, values in zip(keys, freqs, data[3:]):
            self.signalData[name] = [float(x) for x in values.split(sep=",")]
            self.signalFreq[name] = int(freq)
        file.close()
    
    def save(self):
        """Save data to self.path"""
        file = open(self.path, "w")
        freqs = []
        datalines = []
        for name in self.signalData.keys():
            freqs.append(self.signalFreq[name])
            datalines.append(','.join([str(x) for x in self.signalData[name]]))
        names = ','.join([str(x) for x in self.signalData.keys()])
        freqs = ','.join([str(x) for x in freqs])
        file.write(names + "\n")
        file.write(freqs + "\n\n")
        file.writelines(line + "\n" for line in datalines)
        file.close()

    def __str__(self):
        output = ""
        for name in self.signalData.keys():
            output += name + " " + str(self.signalFreq[name]) + ": " + ",".join([str(x) for x in self.signalData[name]]) + "\n"
        return output

    def add_signal(self, signalName:str, signalFreq:float, signalData:List[float] = []):
        """Add new signal to DataStore."""
        self.signalData[signalName] = signalData
        self.signalFreq[signalName] = signalFreq
    
if __name__ == "__main__":
    # For testing
    testCSV = open("./test.csv", "w")
    testData = """s1,s2,s3,s4
5,100,500,1000

1,2,3,4
5,6,7,8
9,10,11,12
13,14,15,16
"""
    testCSV.write(testData)
    testCSV.close()
    data = DataStore("./test.csv")
    print(data)
    data.save()
    data.add_signal("s5", 2000, [17, 18, 19, 20])
    print(data)