# https://github.com/2dof/esp_control
#The MIT License (MIT), Copyright (c) 2022-2023 L.Szydlowski
# __version__   = "1.0.0"


import array
from lookup_search import idx_search


# 0 - 760 C
ITS90_EJ=array.array('H',[2059,4187,6360,8562,10779,13000,15219,
  17434,19642,21848,24057,26276,28516,30788,33102,35470,37896,40382,42919])

  
def its90_J_lookup(E,low=0, high=19):

    idx =idx_search(ITS90_EJ,low,high, E)
    if idx==-1: 
        a=40/(ITS90_EJ[0]) 
        y = a*E   

    else:
        a=40/(ITS90_EJ[idx+1]-ITS90_EJ[idx]) 
        y = a*(E-ITS90_EJ[idx])+(idx+1)*40
        
    return y,idx 

  
# if __name__ == '__main__':
# 
#     
#     E   = [-2431,-501,0,507,1019,1537,2059,12445,13555,15773,16604,16881,22400,27673,29080,29307,29647,33102,42919,45494,51877,57953,69553] # [uV]
#     Tref= [-50,-10, 0, 10, 20, 30, 40,230,250,290,305,310,410,505, 530, 534,540 ,600,760,800,900, 1000, 1210]
#      
#  
# 
#     for i in range(len(E)):
#         T,idx = its90_J_lookup(E[i])
#         print(Tref[i],T)
    
