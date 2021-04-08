import numpy as np
from numpy import random

def chooseProton(hitCount,hitsNucleus,pathFiles,max_hit):
    cell_count=len(hitCount)  # the hitcount is a matrix with rows for cells
    file = open(pathFiles,'r')  # import the text file for the protons of interest
    Tracks=file.readlines()

    for i in range(len(Tracks)):
            # make the strings into floats for easy handeling
            Tracks[i]=float(Tracks[i].replace('.root\n', ''))

    #max_hit=35000#max(hitCount)  # assumed maximum hits per cell
    hitMartix=np.zeros((cell_count,max_hit))  # a row is a cell and #collom is for each cell
    hitMatrixNucleus=np.zeros((cell_count,max_hit))
    for i in range(cell_count):
        hitMartix[i,0:int(hitCount[i])]=random.choice(Tracks,size=int(hitCount[i]))
        # the hit matrix is the same dim as the cell matrix. gives each hit its own proton
        hitMatrixNucleus[i,0:int(hitsNucleus[i])]=hitMartix[i,0:int(hitsNucleus[i])]#random.choice(Tracks,size=int(hitsNucleus[i]))

    return hitMartix,hitMatrixNucleus


if __name__=='__main__':
    hitCount= [6,2,3,4,5,6,7,8]
    hitMartix=chooseProton(hitCount)
    for i,x in enumerate(hitMartix):
        print(x,i)
