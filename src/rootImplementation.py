import numpy as np; import uproot

from src.numberofion import NumberOfIon
from src.Plot import PlotNumIonPerCell
from src.LET import LETfunc
from src.DosePerCell import DosePerCell
def TingTarTid(pathData,x_rad,y_rad,hitMatrix,h_cell,ProtDrawM,LET,NumIon,DoseCell):
    # start of with declaring some varriables
    root='.root'
    path=pathData
    unique=np.unique(ProtDrawM)  # check for unique elements in the proton matrix
    unique=unique[unique!=0].astype(int)  # no proton is named 0 and make the array int to work
    h_cell=h_cell*1e3
    """
    to get info from root files
    ['flagParticle', 'flagProcess',
     'x', 'y', 'z', 'totalEnergyDeposit',
     'stepLength', 'kineticEnergyDifference',
     'kineticEnergy', 'cosTheta', 'eventID',
     'trackID', 'parentID', 'stepID']
    """
    # define the different arrays for data accumulation
    PerCellArrayIon=np.zeros_like(ProtDrawM)
    PerCellArrayExi=np.zeros_like(ProtDrawM)
    LET_array=np.zeros(5)
    DoseCellM=np.zeros_like(ProtDrawM)
    for i,x in enumerate(unique):
        specific_cell_index=np.where(ProtDrawM==x)  # where is the proton in question
        file=uproot.open(path+'/'+str(x)+root)['microdosimetry']  # open the specific file.root for that specific proton
        z=file['z'].array()  # distance traveld
        #print(z[0],h_cell)
        #h_cell=h_cell*10**3+z[0]  # height of cell pluss incident proton position
        h_index=np.where(z<h_cell)  # exclude the interactions larger than the cell, h-index is the index for these interactions
        print(i,x)
        if LET=='y':
            energy=file['totalEnergyDeposit'].array()
            process=file['flagProcess'].array()
            tempLET=LETfunc(energy,z,h_cell,process)
            LET_array=LET_array+tempLET
        if NumIon=='y':
            process=file['flagProcess'].array()
            PerCellArrayIon,PerCellArrayExi=NumberOfIon(z,h_cell,process,PerCellArrayIon,
                                                        PerCellArrayExi,specific_cell_index)
        if DoseCell=='y':
            energy=file['totalEnergyDeposit'].array()
            process=file['flagProcess'].array()
            DoseCellM=DosePerCell(z,h_cell,process,energy,DoseCellM,
                                    specific_cell_index)



        print('progress: {}%'.format(int(float(100)/len(unique)*i)))


    totIonPerCell=np.sum(PerCellArrayIon,axis=1)
    totExiPerCell=np.sum(PerCellArrayExi,axis=1)
    totDoseCellM = np.sum(DoseCellM,axis=1)
    LET_array=LET_array/len(unique)
    return totIonPerCell,totExiPerCell,LET_array,totDoseCellM
