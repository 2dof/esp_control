# https://github.com/2dof/esp_control
#The MIT License (MIT), Copyright (c) 2022-2023 L.Szydlowski
# __version__   = "1.0.0"


import array
from lookup_search import idx_search
from benchmark import timed_function
import gc

gc.collect()
start = gc.mem_free()
ITS90_EJ=array.array('H',[2059,4187,6360,8562,10779,13000,15219,
  17434,19642,21848,24057,26276,28516,30788,33102,35470,37896,40382,42919])
print(start - gc.mem_free())




@timed_function    
def its90_J_lookup(E,low=0, high=19):

    idx =idx_search(ITS90_EJ,low,high, E)
    if idx==-1: 
        a=40/(ITS90_EJ[0]) 
        y = a*E   

    else:
        a=40/(ITS90_EJ[idx+1]-ITS90_EJ[idx]) 
        y = a*(E-ITS90_EJ[idx])+(idx+1)*40
        
    return y,idx 


if __name__ == '__main__':

#     Ei =69553 # 1210
#     Ei= 57953 # 1000 C
#     Ei= 51877 # 900 C
#     Ei= 45494 # 800 
#     Ei= 42919 # 760 
#     Ei= 33102 # 600
#     Ei=29647   # 540 
#     Ei=29307 # 534
#     Ei=29080  # 530
#     Ei= 27673 # 505
#     Ei= 22400 # 410
#     Ei= 16881 # 310
#     Ei= 16604  # 305
#     Ei= 15773  # 290
#     Ei=13555 # 250 
#     Ei= 12445  # 230
#     Ei= 2059 # 40 
#     Ei= 1537 # 30 
#     Ei= 1019  #20
#     Ei = 507  # 10
#     #Ei = 0.0# 0 
#     #Ei=-501 # -10
#     #Ei=-2431 # -50
#     print(its90_J_lookup(Ei)[0])
    
    E   = [-2431,-501,0,507,1019,1537,2059,12445,13555,15773,16604,16881,22400,27673,29080,29307,29647,33102,42919,45494,51877,57953,69553] # [uV]
    Tref= [-50,-10, 0, 10, 20, 30, 40,230,250,290,305,310,410,505, 530, 534,540 ,600,760,800,900, 1000, 1210]
     
 
# 
    for i in range(len(E)):
        T,idx = its90_J_lookup(E[i])
 
        #print(Tref[i],T)
#     
    
