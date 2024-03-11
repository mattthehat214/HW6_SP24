from scipy.optimize import fsolve

RESISTOR = "resistor"
SOURCE = "source"
LOOP = "loop"

class ResistorNetwork():
    def __init__(self):
        self.Loops = []  
        self.Resistors = []  
        self.VSources = []  


    """
    This is the construction for the network and definition of loops
    """
    def BuildNetworkFromFile(self, filename):
        with open(filename,"r") as file:
            file_content = file.read().split('\n')
        line_number = 0
        self.Resistors = []
        self.VSources = []
        self.Loops = []
        while line_number < len(file_content):
            line_text = file_content[line_number].lower().strip()
            if line_text.startswith('#') or not line_text:
                line_number += 1
                continue
            if RESISTOR in line_text:
                line_number = self.MakeResistor(line_number, file_content)
            elif SOURCE in line_text:
                line_number = self.MakeVSource(line_number, file_content)
            elif LOOP in line_text:
                line_number = self.MakeLoop(line_number, file_content)
            line_number += 1

    def MakeResistor(self, line_number, file_content):
        R = Resistor()  
        line_number += 1  
        line_text = file_content[line_number].lower().strip()  
        while RESISTOR not in line_text:
            if "name" in line_text:
                R.Name = line_text.split('=')[1].strip()
            if "resistance" in line_text:
                R.Resistance = float(line_text.split('=')[1].strip())
            line_number += 1
            if line_number < len(file_content): 
                line_text = file_content[line_number].lower()
            else:
                break
        self.Resistors.append(R)  
        return line_number

    def MakeVSource (self, line_number, file_content):
        VS = VoltageSource()
        line_number += 1
        line_text = file_content[line_number].lower()
        while SOURCE not in line_text:
            if "name" in line_text:
                VS.Name = line_text.split('=')[1].strip()
            if "value" in line_text:
                VS.Voltage = float(line_text.split('=')[1].strip())
            if "type" in line_text:
                VS.Type = line_text.split('=')[1].strip()
            line_number += 1
            line_text = file_content[line_number].lower()
        self.VSources.append(VS)
        return line_number

    def MakeLoop(self, line_number, file_content):
        L = Loop()
        line_number += 1
        line_text = file_content[line_number].lower()
        while LOOP not in line_text:
            if "name" in line_text:
                L.Name = line_text.split('=')[1].strip()
            if "nodes" in line_text:
                line_text = line_text.replace(" ","")
                L.Nodes = line_text.split('=')[1].strip().split(',')
            line_number += 1
            line_text = file_content[line_number].lower()
        self.Loops.append(L)
        return line_number

    def AnalyzeCircuit(self):
        currents_initial_guess = [0.1]*len(self.Resistors)
        currents = fsolve(self.GetKirchoffVals, currents_initial_guess)
        for idx, current in enumerate(currents, start=1):
            print(f"I{idx} = {current:.1f}")
        return currents

"""
Process of the files for said loops
"""
    
    def GetKirchoffVals(self, currents):
        self.GetResistorByName('ad').Current = currents[0]
        self.GetResistorByName('bc').Current = currents[0]
        self.GetResistorByName('cd').Current = currents[2]
        self.GetResistorByName('ce').Current = currents[1]
        Node_c_Current = sum([currents[0], currents[1], -currents[2]])
        KVL = self.GetLoopVoltageDrops()
        KVL.append(Node_c_Current)
        return KVL

    def GetElementDeltaV(self, name):
        for r in self.Resistors:
            if name == r.Name or name[::-1] == r.Name:
                return -r.DeltaV()
        for v in self.VSources:
            if name == v.Name or name[::-1] == v.Name:
                return v.Voltage

    def GetLoopVoltageDrops(self):
        loopVoltages = []
        for L in self.Loops:
            loopDeltaV = 0
            for n in range(len(L.Nodes)):
                if n == len(L.Nodes)-1:
                    name = L.Nodes[0] + L.Nodes[n]
                else:
                    name = L.Nodes[n] + L.Nodes[n+1]
                loopDeltaV += self.GetElementDeltaV(name)
            loopVoltages.append(loopDeltaV)
        return loopVoltages

    def GetResistorByName(self, name):
        for r in self.Resistors:
            if r.Name == name:
                return r

class Loop():
    def __init__(self):
        self.Nodes = []

class Resistor():
    def __init__(self, R=1.0, i=0.0, name='ab'):
        self.Resistance = R
        self.Current = i
        self.Name = name

    def DeltaV(self):
        return self.Current*self.Resistance

class VoltageSource():
    def __init__(self, V=12.0, name='ab'):
        self.Voltage = V
        self.Name = name

def main():
    Net = ResistorNetwork()  
    Net.BuildNetworkFromFile('ResistorNetwork.txt')
    IVals = Net.AnalyzeCircuit()
    print(f"Calculated I for 1,2,3:{IVals} A")

if __name__=="__main__":
    main()
