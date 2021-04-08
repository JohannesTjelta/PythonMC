def dose(Gy,mean_energy_dep):
    eV=1.60218e-19  # ev to Joule
    volume =  1.161e-5  # mass of volume in kg -> 1.161e-5:  cell nucleus volume -> 1.131e-13
    deposit2Joule = eV*mean_energy_dep
    numberProt = Gy*volume/deposit2Joule
    print(numberProt)
    return int(numberProt)
