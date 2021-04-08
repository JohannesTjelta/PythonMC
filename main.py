import numpy as np
import matplotlib.pyplot as plt
from numba import jit, cuda
from timeit import default_timer as timer

from src.Files import FilesOfInterest
from src.Dose import dose
from src.Montecarlo import MC
from src.CellDist import celldist
from src.Interaction import interaction
from src.protonChoice import chooseProton
from src.rootImplementation import TingTarTid
from src.Plot import PlotNumIonPerCell,PlotLET, PlotDoseCell,Dosedist,PlotNumIonPerNuc,PlotDoseNuc

y='y'
n='n'

print('\n\n-----------------------------------------------------------------------')
Enter_energy = float(input('Enter proton energy [MeV] (8.0=1,1.8=2,1.4=3,1.2=4):'))
print('-----------------------------------------------------------------------')
"""
First coupple of lines is a if test to declare the energy
which shall be used and the location of the protons of interest
, furthermore the mean ernergy deposit per proton per 4um is declared
"""
if Enter_energy==1:
    pathFiles='Data8/Res/FilesOfInterest.txt'
    pathData='Data8'
    name = '8MeV'
    mean_energy_dep=15078.96  # now ok
elif Enter_energy==2:
    pathFiles='Data1_8/Res/FilesOfInterest.txt'
    pathData='Data1_8'
    name='1_8MeV'
    mean_energy_dep=57960.49666363634 # new value changed 02,03,21#67788.38  # now ok
elif Enter_energy==3: #1.46
    pathFiles='Data1_4/Res/FilesOfInterest.txt'
    pathData='Data1_4'
    name='1_4MeV'
    mean_energy_dep=69045.56688785045#79000#only ion:69000;ion and exi: 79000;tot:101908.50255734059 # now ok
elif Enter_energy==4:
    pathFiles='Data1_2/Res/FilesOfInterest.txt'
    pathData='Data1_2'
    name='1_2MeV'
    mean_energy_dep=75369.00045882349  # now ish ok

print('\n\n-----------------------------------------------------------------------')
d = float(input('Enter dose in Gy:'))
print('-----------------------------------------------------------------------')
numberProt = dose(d,mean_energy_dep)
#numberProt = 2*1e6 # used for testing

print('\n\n-----------------------------------------------------------------------')
NumberCell = int(input('Enter cell count:'))
print('-----------------------------------------------------------------------')
x_cell,y_cell,x_nucleus,y_nucleus=celldist(NumberCell)


print('\n\n-----------------------------------------------------------------------')
print('The cell is aproximated with a sylinder with a height and a radius')
print('-----------------------------------------------------------------------')
r = float(input('\nEnter cell radius [um]:'))
h = float(input('Enter cell height [um]:'))

if h>6:
    print('maximum cell heigt is 5.9um, try agen')
    exit()

print('\n\n-----------------------------------------------------------------------')
print('You will now get a few choises on what you want.\nThis will take time so grab a coffe or take a nap :')
print('\n-----------------------------------------------------------------------')
LET = input('\nDo you want to calculate LET of the protons? (y/n)')
NumIon = input('\nDo you want to calculate the number of ionisations per cell? (y/n)')
DoseCell = input('\nDo you want to calculate the dose per cell? (y/n)')



r_nucleus=6  # implemantet at a later stage, therfor hardcoded in the program

max_hit = 35000 # integer to make hit matrix
x_matrix=np.zeros((NumberCell,max_hit))  # x position for each
y_matrix=np.zeros((NumberCell,max_hit))
x_nucleus_matrix = np.zeros((NumberCell,max_hit))
y_nucleus_matrix = np.zeros((NumberCell,max_hit))
max_prot_per = 10**5
iterations=int(float(numberProt)/max_prot_per)
print(iterations)
hitsCell= np.zeros(len(x_cell))
hitsNucleus= np.zeros(len(x_cell))


for i in range(iterations):
    start = timer()
    x,y = MC(max_prot_per)
    x_matrix,y_matrix,hitsCell,x_nucleus_matrix,y_nucleus_matrix,hitsNucleus=interaction(r,r_nucleus,x,y,x_cell,y_cell,x_matrix,y_matrix,hitsCell,
                                            x_nucleus_matrix,y_nucleus_matrix,hitsNucleus,x_nucleus,y_nucleus)
    x=None;y=None  # free up memory

    print('progress Cell hit reg: {}%'.format(int(float(100)/iterations*i))+"\ntime taken:", timer()-start)

np.savetxt('filesxy/'+name+str(NumberCell)+'cellss'+str(int(d))+'GyCellx.txt',(x_matrix))
np.savetxt('filesxy/'+name+str(NumberCell)+'cellss'+str(int(d))+'GyNucx.txt',(x_nucleus_matrix))
np.savetxt('filesxy/'+name+str(NumberCell)+'cellss'+str(int(d))+'GyCelly.txt',(y_matrix))
np.savetxt('filesxy/'+name+str(NumberCell)+'cellss'+str(int(d))+'GyNucy.txt',(y_nucleus_matrix))

proton_randoom_draw_matrix,proton_randoom_draw_matrix_nucleus = chooseProton(hitsCell,hitsNucleus,pathFiles,max_hit)


totIonPerCell,totExiPerCell,LET_array,totDoseCellM=TingTarTid(pathData,x_matrix,y_matrix,hitsCell
                                                            ,h,proton_randoom_draw_matrix,LET,NumIon,DoseCell)

totIonPerNucleus,totExiPerNucleus,LET_array_nuc,totDoseNucM=TingTarTid(pathData,x_nucleus_matrix,y_nucleus_matrix,hitsNucleus
                                                            ,h,proton_randoom_draw_matrix_nucleus,LET,NumIon,DoseCell)

if NumIon=='y':
    PlotNumIonPerCell(totIonPerCell,totExiPerCell,name,NumberCell,d)
    PlotNumIonPerNuc(totIonPerNucleus,totExiPerNucleus,name,NumberCell,d)
    np.savetxt('DataOut/Ion{}Gy{}cells'.format(d,NumberCell)+name+'.txt',totIonPerCell)
    np.savetxt('DataOut/Exi{}Gy{}cells'.format(d,NumberCell)+name+'.txt',totExiPerCell)
    np.savetxt('DataOut/Ion{}Gy{}cellsNuc'.format(d,NumberCell)+name+'.txt',totIonPerNucleus)
    np.savetxt('DataOut/Exi{}Gy{}cellsNuc'.format(d,NumberCell)+name+'.txt',totExiPerNucleus)

if LET=='y':
    print(LET_array)
    PlotLET(LET_array,name,h,NumberCell)

if DoseCell=='y':
    vol=3.1415*(r*1e-5)**2*h*1e-5
    eV=1.60218e-19
    totDoseCellM=totDoseCellM*eV/vol
    volN=3.1415*(r_nucleus*1e-5)**2*h*1e-5
    totDoseNucM=totDoseNucM*eV/volN
    print('Mean dose per cell: {}Gy'.format(np.mean(totDoseCellM)))
    print('Mean dose per nuc: {}Gy'.format(np.mean(totDoseNucM)))
    np.savetxt('DataOut/Dose{}Gy{}cells'.format(d,NumberCell)+name+'.txt',totDoseCellM)
    np.savetxt('DataOut/Dose{}Gy{}cellsNuc'.format(d,NumberCell)+name+'.txt',totDoseNucM)
    PlotDoseCell(totDoseCellM,name,NumberCell,d)
    PlotDoseNuc(totDoseNucM,name,NumberCell,d)
