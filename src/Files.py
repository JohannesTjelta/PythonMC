import numpy as np

def FilesOfInterest(numberProt,pathFiles):
    n='n'
    y='y'
    FilesOfInterest = open(pathFiles,'r')
    File_array =[]
    for line in FilesOfInterest:
        line=line.replace('.root\n','')
        line = int(line)
        File_array.append(line)

    yay_happy_files = np.random.choice(File_array,numberProt)
    I=input('\nDo you want do save the proton info in a seperate txt file?(y or n)')
    if I=='y':
        f=open('filesxy/yay_happy_files.txt','w')
        np.savetxt(f,yay_happy_files)
        print('The proton info has been saved to filesxy as yay_happy_files')
    else:
        print('ok :)')
    return File_array
