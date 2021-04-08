import numpy as np

def NumberOfIon(z,dz,process,PerCellArrayIon,PerCellArrayExi,specific_cell_index):
    PerCellArrayIon[specific_cell_index]=len(process[np.where((z>z[0])&(z<z[0]+dz)&((process==13)|(process==23)))])
    PerCellArrayExi[specific_cell_index]=len(process[np.where((z>z[0])&(z<z[0]+dz)&((process==12)|(process==22)))])

    return PerCellArrayIon,PerCellArrayExi
