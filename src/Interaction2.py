import numpy as np
import scipy.spatial as s
from numba import jit



@jit
def interaction(r,r_nucleus,x,y,x_cell,y_cell,x_matrix,y_matrix,hitsCell,x_nucleus_matrix,y_nucleus_matrix,hitsNucleus,x_nucleus,y_nucleus):

    r=r*1e-4
    r_nucleus=r_nucleus*1e-4
    # from cm to um
    cells_xy=np.column_stack((x_cell,y_cell))
    prot_xy=np.column_stack((x,y))
    max_hit = 10000 # integer to make hit matrix
    cell_count = len(x_cell)  # rows in matrix corresponds co cells
    dist = s.distance.cdist(cells_xy,prot_xy,metric='euclidean')  # distance between cell center and protons
    inCell,prot_num=np.where(dist<r)  # check if proton is whithin a cell
    inNucleus,prot_numN=np.where(dist<r_nucleus)

    for j,i in enumerate(inCell):
        hitsCell[i]+=1
        first_zero_value_index=np.where(x_matrix[i,:]==0)
        first_zero_value=first_zero_value_index[0]
        x_matrix[i,first_zero_value[0]:first_zero_value[0]+1]=x[prot_num[j]]
        y_matrix[i,first_zero_value[0]:first_zero_value[0]+1]=y[prot_num[j]]

    for j,i in enumerate(inNucleus):
        hitsNucleus[i]+=1
        first_zero_value_index_nucleus=np.where(x_nucleus_matrix[i,:]==0)
        first_zero_value_nucleus=first_zero_value_index_nucleus[0]
        x_nucleus_matrix[i,first_zero_value_nucleus[0]:first_zero_value_nucleus[0]+1]=x[prot_numN[j]]
        y_nucleus_matrix[i,first_zero_value_nucleus[0]:first_zero_value_nucleus[0]+1]=y[prot_numN[j]]


    return x_matrix,y_matrix,hitsCell,x_nucleus_matrix,y_nucleus_matrix,hitsNucleus
