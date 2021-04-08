import numpy as np
def MC(numberProt):
    n='n'
    y='y'
    def invert_int_func(a,y,b):  # inverted cpd
        return np.sqrt(2*a*y+b**2)/a

    slope = 0.2135106133113824  # slope for the model
    intercept = 0.00  # intercept for the model

    Y = np.random.rand(numberProt).astype('float64')  # Check cell dist to se explenation
    r = invert_int_func(slope,Y,intercept)
    deg = np.random.rand(numberProt).astype('float64')*2*np.pi

    def pol2cart(rho, phi):
        x = rho * np.cos(phi)
        y = rho * np.sin(phi)
        return(x, y)

    x_dist,y_dist=pol2cart(r,deg)
    return x_dist,y_dist
