# https://github.com/2dof/esp_control
#The MIT License (MIT), Copyright (c) 2022-2023 L.Szydlowski
# __version__   = "1.0.0"

import array
from benchmark import timed_function

import gc
# 
gc.collect()
start = gc.mem_free()
# all polybomials 104 bytes but as arrays 672)
 
 
 
# # -8,095μV to 0 μV (-210 - 0 C )
_CJi0 =array.array('f',[0.0000000,
                1.9528268*1e-2,
                -1.2286185*1e-6,
                -1.0752178*1e-9,
                -5.9086933*1e-13,
                -1.7256713*1e-16,
                -2.8131513*1e-20,
                -2.3963370*1e-24,
                -8.3823321*1e-29])
# # 0 μV to 42919 μV  (0-760 C)
_CJi1=array.array('f',[0.000000,
                1.978425*1e-2,
                -2.001204*1e-7,
                1.036969*1e-11,
                -2.549687*1e-16,
                3.585153*1e-21,
                -5.344285*1e-26,
                5.099890*1e-31])
# # 42919 to 69553 μV (760 -1210 C)
_CJi2=array.array('f',[-3.11358187*1e3,
                3.00543684*1e-1,
                -9.94773230*1e-6,
                1.70276630*1e-10,
                -1.43033468*1e-15,
                4.73886084*1e-21])

print(start - gc.mem_free())

@timed_function
def its90_J(E):
    
    
    Ev = 1.
    T=0.0
    if E > 42919: # 42919 to 69553  μV (760 -1210 C)
        T =_CJi2[0]
        
        for i in range(1,6):
            Ev*=E
            T+=_CJi2[i]*Ev
            
    elif E <= 0.:        #(-210 - 0 C )
          T =_CJi0[0]
          for i in range(1,9):
            Ev*=E  
            T+=_CJi0[i]*Ev 
            
             
    else: # 0 μV to 42919 μV  (0-760 C)

        T =_CJi1[0]
        
        for i in range(1,8):
            Ev*=E
            T+=_CJi1[i]*Ev 
            
    return T  

if __name__ == '__main__':
# 
    E   = [-2431,-501,0,507,1019,1537,2059,12445,13555,15773,16604,16881,22400,27673,29080,29307,29647,33102,42919,45494,51877,57953,69553] # [uV]
    Tref= [-50,-10, 0, 10, 20, 30, 40,230,250,290,305,310,410,505, 530, 534,540 ,600,760,800,900, 1000, 1200]


    for i in range(len(E)):
        T= its90_J(E[i])
        #print(Tref[i],T)