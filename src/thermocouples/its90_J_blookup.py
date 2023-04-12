# https://github.com/2dof/esp_control
#The MIT License (MIT), Copyright (c) 2022-2023 L.Szydlowski
# __version__   = "1.0.0"


#import array
from lookup_search import bytes_search

# -0....760 , every 40 C 
_ITS90_EJB = b'\x0b\x08[\x10\xd8\x18r!\x1b*\xc82s;\x1aD\xbaLXU\xf9]\xa4fdoDxN\x81\x8e\x8a\x08\x94\xbe\x9d\xa7\xa7'

def its90_J_blookup(E,low=0, high=19):
    
    idx = bytes_search(_ITS90_EJB,low,high, E)
    
    if idx==-1:
        y=(0.01943*E) if E<2059 else (0.01577*E + 83)
    else:
        i=2*idx
        v1=int.from_bytes(_ITS90_EJB[i:(i+2)], 'little') 
        a=40/(int.from_bytes(_ITS90_EJB[(i+2):(i+4)], 'little') -v1)
        y= a*(E-v1)+(idx+1)*40
        
    return y,idx

#if __name__ == '__main__':
# 
#    E   = [-2431,-501,0,507,1019,1537,2059,12445,13555,15773,16604,16881,22400,27673,29080,29307,29647,33102,42919,45494,51877,57953,69553] # [uV]
#    Tref= [-50,-10, 0, 10, 20, 30, 40,230,250,290,305,310,410,505, 530, 534,540 ,600,760,800,900, 1000, 1210]
     
#    for i in range(len(E)):
#        T,idx = its90_J_blookup(E[i])
#        print(Tref[i],T)
        
