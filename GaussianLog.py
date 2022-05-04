import pandas as pd
import numpy as np
import glob

class GaussianLog():
    def __init__(self, data_sp, Temp):
        self.data_sp = data_sp
        self.Temp = Temp
    
    def electronic_energy(self):
        for i in range(len(self.data_sp)):
            if "SCF Done:" in self.data_sp[i]:
                EE = self.data_sp[i]
                EE = EE.strip("SCF Done:")
                EE = EE.split()
                EE = EE[2]
                EE = float(EE) * 2625.5 # convert kJ/mol
        return EE
    
    def gibbs(self):
        for i in range(len(self.data_sp)):
            if "Sum of electronic and thermal Free Energies=" in self.data_sp[i]:
                G = self.data_sp[i]
                G = G.strip("Sum of electronic and thermal Free Energies=")
                G = G.split()
                G = G[0]
                G = float(G) + 2625.5
        return G
    
    def trans(self):
        for i in range(len(self.data)):
            if "Translational      " in self.data_sp[i]:
                E_tr = self.data_sp[i]
                E_tr = E_tr.strip("Translational      ")
                E_tr = E_tr.split()
                S_tr = E_tr[2]
                E_tr = E_tr[0]
                E_tr = float(E_tr) * 4.184
                S_tr = float(S_tr) * self.Temp * 4.184 * 0.001 * (-1)
        return E_tr, S_tr
    
    def vib(self):
        for i in range(len(self.data_sp)):
            if "Vibrational      " in self.data_sp[i]:
                E_vib = self.data_sp[i]
                E_vib = E_vib.split("Vibrational      ")
                E_vib = E_vib.split()
                S_vib = E_vib[2]
                E_vib = E_vib[0]
                E_vib = float(E_vib) * 4.184
                S_vib = float(S_vib) * self.Temp * 4.184 * (-1)
        return E_vib, S_vib    

    def rot(self):
        for i in range(len(self.data_sp)):
            if "Rotational      " in self.data_sp[i]:
                E_rot = self.data_sp[i]
                E_rot = E_rot.strip("Rotational      ")
                E_rot = E_rot.split()
                S_rot = E_rot[2]
                E_rot = E_rot[0]
                E_rot = float(E_rot) * 4.184
                S_rot = float(S_rot) * self.Temp * 4.184 * 0.001 * (-1)
        return E_rot, S_rot



le = glob.glob("*.log")

lst_name = []
lst_EE = []
lst_G = []
lst_transE = []
lst_rotE = []
lst_vibE = []
lst_transG = []
lst_rotG = []
lst_vibG = []


for i in range(len(le)):
    f = open(le[i])
    data = f.read()
    f.close
    data_sp = data.split('¥n')
    name = le[i][:-4]
    lst_name.append(name)
    ins = GaussianLog(data_sp, 298.15) ### Temperature
    

    EE = ins.electronic_energy()
    lst.EE.append(EE)
    
    transE, transG = ins.trans()
    lst_transE.append(transE)
    lst_transG.append(transG)
    
    rotE, rotG = ins.rot()
    lst_rotE.append(rotE)
    lst_rotG.append(rotG)
    
    vibE, vibG = ins.vib()
    lst_vibE.append(vibE)
    lst_vibG.append(vibG)
    

column = ["name", "EE", "G", "transE", "transG", "rotE", "rotG", "vibE", "vibG"]
df = pd.DataFrame(columns=column)
df["name"] = lst_name
df["EE"] = lst_EE
df["G"] = lst_G
df["transE"] = lst_transE
df["transG"] = lst_transG
df["rotE"] = lst_rotE
df["rotG"] = lst_rotG
df["vibE"] = lst_vibE
df["vibG"] = lst_vibG

df.to_csv("log_results.csv")
