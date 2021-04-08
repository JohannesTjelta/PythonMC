import numpy as np
import random
import matplotlib.pyplot as plt
def celldist(NumberCell):
    x_cell=np.zeros(NumberCell)
    y_cell=np.zeros(NumberCell)
    i=0
    while i<NumberCell:
        x_temp=random.uniform(-3,3)
        y_temp=random.uniform(-3,3)
        d =  np.sqrt(x_temp*x_temp+y_temp*y_temp)
        if d> 3:
            None
        elif d<3:
            x_cell[i]= x_temp
            y_cell[i]=y_temp
            i+=1
        if i==NumberCell:
            x_nucleus=x_cell
            y_nucleus=y_cell
            break

    return x_cell,y_cell,x_nucleus,y_nucleus

if __name__=='__main__':
    cellMatrix=celldist(100000)
    #print(cellMatrix)
    plt.plot(cellMatrix[0],cellMatrix[1],'.')

    radiel=np.zeros(len(cellMatrix[1]))

    radiel=np.sqrt(cellMatrix[1]**2+cellMatrix[0]**2)
    plt.figure()
    plt.hist(radiel,density=True)
    plt.show()
