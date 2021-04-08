import numpy as np
from numba import jit,cuda,vectorize

def interaction(r,r_nucleus,x,y,x_cell,y_cell,x_matrix,y_matrix,hitsCell,x_nucleus_matrix,y_nucleus_matrix,hitsNucleus,x_nucleus,y_nucleus):
    r=r*1e-4
    r_nucleus=r_nucleus*1e-4
    # from cm to um
    max_hit = 10000 # integer to make hit matrix
    cell_count = len(x_cell)  # rows in matrix corresponds co cells
    for i in range(len(x_cell)):  # for loop for cell
        @vectorize(['float64(float64,float64,float64,float64)'],target='cuda')
        def dist(x,x_cell,y,y_cell):
            dist = np.sqrt((x-x_cell)**2+(y-y_cell)**2)  # distance between cell center and protons
            return dist
        dist = dist(x,x_cell,y,y_cell)
        inCell=np.where(dist<r)  # check if proton is whithin a cell

        numHits = len(inCell[0])  # number of hits per cell
        first_zero_value_index=np.where(x_matrix[i,:]==0)
        first_zero_value=first_zero_value_index[0]

        x_matrix[i,first_zero_value[0]:numHits+first_zero_value[0]]=x[inCell]
        y_matrix[i,first_zero_value[0]:numHits+first_zero_value[0]]=y[inCell]

        hitsCell[i]+=numHits  # number of hits per cell corresponding to row in matrix

    for i in range(len(x_cell)):  # for loop for nucleus
        #dist_nucleus = np.sqrt((x-x_nucleus[i])**2+(y-y_nucleus[i])**2)  # distance between nucleus center and protons

        inCell_nucleus=np.where(dist<r_nucleus)  # check if proton is whithin a nucleus
        numHits_nucleus = len(inCell_nucleus[0])  # number of hits per nucleus

        first_zero_value_index_nucleus=np.where(x_nucleus_matrix[i,:]==0)
        first_zero_value_nucleus=first_zero_value_index_nucleus[0]

        x_nucleus_matrix[i,first_zero_value_nucleus[0]:numHits_nucleus+first_zero_value_nucleus[0]]=x[inCell_nucleus]
        y_nucleus_matrix[i,first_zero_value_nucleus[0]:numHits_nucleus+first_zero_value_nucleus[0]]=y[inCell_nucleus]

        hitsNucleus[i]+=numHits_nucleus

    return x_matrix,y_matrix,hitsCell,x_nucleus_matrix,y_nucleus_matrix,hitsNucleus
