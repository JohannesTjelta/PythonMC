import numpy as np

def LETfunc(ener,z,h,process):
    energy = ener[np.where((z>z[0])&(z<z[0]+h)&((process==12)|(process==13)|(process==22)|(process==23)))]
    z= z[np.where((z>z[0])&(z<z[0]+h)&((process==12)|(process==13)|(process==22)|(process==23)))]
    dz= np.linspace(z[0],z[-1],5)
    tempLET=np.zeros(len(dz))
    for i in range(len(dz)-1):
        tempLET[i]=np.sum(ener[np.where((z>dz[i])&(z<dz[i+1]))])
    return tempLET
