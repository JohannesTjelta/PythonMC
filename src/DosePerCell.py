import numpy as np

def DosePerCell(z,dz,process,energy,DoseCellM,specific_cell_index):
    DoseCellM[specific_cell_index]=sum(energy[np.where((z>z[0])&(z<z[0]+dz)&((process==12)|(process==13)|(process==22)|(process==23)))])
    return DoseCellM
