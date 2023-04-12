# https://github.com/2dof/esp_control
#The MIT License (MIT), Copyright (c) 2022-2023 L.Szydlowski
# __version__   = "1.0.0"

import array
from benchmark import timed_function

from model_J import its90model_J



E   = [-2431,-501,0,507,1019,1537,2059,12445,13555,15773,16604,16881,22400,27673,29080,29307,29647,33102,42919,45494,51877,57953,69553] # [uV]
T   = [-50,-10, 0, 10, 20, 30, 40,230,250,290,305,310,410,505, 530, 534,540 ,600,760,800,900, 1000, 1210]


if __name__ == '__main__':
    
    
    print('testing: its90model_J:')
    print('i,Eref,E,err')
    
    for i in range(len(E)):
        Ei = its90model_J(T[i])
        print(i,E[i],Ei,' err:',E[i]-Ei)