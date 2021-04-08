import matplotlib.pyplot as plt
import numpy as np



def Dosedist(x,y,d):
    plt.figure()
    plt.hist2d(x,y,bins=800)
    plt.xlabel('donno')
    plt.ylabel('donno')
    plt.title('2D Histogram of distrebution of {} Gy '.format(d))
    plt.savefig('Plots/2dhistprotondist.PNG')

def PlotNumIonPerCell(totIonPerCell,totExiPerCell,name,NumberCell,d):
    plt.figure()
    plt.hist(totIonPerCell,alpha=0.5,bins=40,color='blue',label='Ion')
    plt.hist(totExiPerCell,alpha=0.5,bins=15,color='red',label='Exi')
    plt.legend()
    plt.title('total ion and exi per cell for {} cells at {}Gy'.format(len(totIonPerCell),d))
    plt.ylabel('cell count')
    plt.xlabel('Events')
    plt.grid()
    plt.savefig('Plots/totExiPerCell'+name+'{}cells{}Gy.PNG'.format(NumberCell,d))
    print('\nPlot for ionisations per cell has been saved to Plots as totIonPerCell.PNG')

def PlotNumIonPerNuc(totIonPerCell,totExiPerCell,name,NumberCell,d):
    plt.figure()
    plt.hist(totIonPerCell,alpha=0.5,bins=40,color='blue',label='Ion')
    plt.hist(totExiPerCell,alpha=0.5,bins=15,color='red',label='Exi')
    plt.legend()
    plt.title('total ion and exi per nucleus for {} cells {}Gy'.format(len(totIonPerCell),d))
    plt.ylabel('cell count')
    plt.xlabel('Events')
    plt.grid()
    plt.savefig('Plots/totExiPerNuc'+name+'{}cells{}Gy.PNG'.format(NumberCell,d))
    print('\nPlot for ionisations per cell has been saved to Plots as totIonPerNuc.PNG')

def PlotLET(LET,name,h,NumberCell):
    plt.figure()
    plt.plot(np.linspace(0,h,len(LET)-1),LET[:-1],'.')
    plt.grid()
    plt.xlabel('um')
    plt.ylabel('keV/um')
    plt.title('LET')
    plt.savefig('Plots/LET'+name+'{}cells.PNG'.format(NumberCell))
    print('\nLet plot has been saved as Plots/LET'+name+'{}cells.PNG'.format(NumberCell))

def PlotDoseCell(totDoseCellM,name,NumberCell,d):
    plt.figure()
    plt.hist(totDoseCellM,alpha=0.7,bins=30,color='blue')
    plt.ylabel('cell count')
    plt.xlabel('Total dose per cell [Gy]')
    plt.grid()
    plt.savefig('Plots/DoseForCells'+name+'{}cells{}Gy.PNG'.format(NumberCell,d))
    print('\nPlot for dose per cell has been saved to Plots as Plots/DoseForCells'+name+'{}cells.PNG'.format(NumberCell))

def PlotDoseNuc(totDoseCellM,name,NumberCell,d):
    plt.figure()
    plt.hist(totDoseCellM,alpha=0.7,bins=30,color='blue')
    plt.ylabel('cell count')
    plt.xlabel('Total dose per nucleus [Gy]')
    plt.grid()
    plt.savefig('Plots/DoseForNuc'+name+'{}cells{}Gy.PNG'.format(NumberCell,d))
    print('\nPlot for dose per cell has been saved to Plots as Plots/DoseForCells'+name+'{}cells.PNG'.format(NumberCell))
