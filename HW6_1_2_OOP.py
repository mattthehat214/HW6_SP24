from HW6_1_OOP import ResistorNetwork, Resistor, VoltageSource, Loop
from scipy.optimize import fsolve

class ResistorNetwork2(ResistorNetwork):
    def __init__(self):
        super().__init__()
        self.Loops = []  
        self.Resistors = []  
        self.VSources = []  

"""
We are grabbing our information from ResistorNetwork2.
We are using len and fsolve to find currents in the network
"""
    
    def AnalyzeCircuit(self):
        currents_initial_guess = [1]*len(self.Resistors)
        currents, info, ier, msg = fsolve(self.GetKirchoffVals, currents_initial_guess, full_output=True)
        if ier != 1:
            print(f"fsolve did not converge, message: {msg}")
        else:
            for idx, current in enumerate(currents, start=1):
                print(f"I{idx} = {current:.1f}A")
        return currents

"""
We are using Kirchoff voltage laws and Kirchoff current laws for the following circuit
"""
    
    def GetKirchoffVals(self, currents):
        self.GetResistorByName('ad').Current = currents[0]
        self.GetResistorByName('bc').Current = currents[0]
        self.GetResistorByName('ce').Current = currents[4]
        self.GetResistorByName('de').Current = currents[3]
        self.GetResistorByName('cd').Current = currents[2]

        Node_c_Current = sum([currents[4], -currents[2], currents[0]])
        Node_d_Current = sum([-currents[1], currents[2], -currents[0], currents[3]])

        KVL = self.GetLoopVoltageDrops()
        KVL.append(Node_c_Current)
        KVL.append(Node_d_Current)

        return KVL

"""
This help us get the final output to get all the current and volatge for the network
"""

def main():
    net = ResistorNetwork2()
    net.BuildNetworkFromFile('ResistorNetwork_2.txt')
    currents = net.AnalyzeCircuit()
    print(f"Calculated currents for 1-5 : {[f'{current:.1f}A' for current in currents]}")

if __name__ == "__main__":
    main()
  
