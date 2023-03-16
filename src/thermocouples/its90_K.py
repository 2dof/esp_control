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
_CKi0 =array.array('f',[0.0000000,
        2.5173462e-2,
        -1.1662878e-6,
        -1.0833638e-9,
        -8.9773540e-13,
        -3.7342377e-16,
        -8.6632643e-20,
        -1.0450598e-23,
        -5.1920577e-28])
# 0 μV to 20,644 μV  (0-500 C)
_CKi1=array.array('f',[0.000000,
       2.508355e-2,
       7.860106e-8,
      -2.503131e-10,
       8.315270e-14,
      -1.228034e-17,
       9.804036e-22,
      -4.413030e-26,
       1.057734e-30,
      -1.052755e-35])
# 20,644 to 54,886 μV (500 -1373 C)
_CKi2=array.array('f',[-1.318058e2,
        4.830222e-2,
       -1.646031e-6,
        5.464731e-11,
       -9.650715e-16,
        8.802193e-21,
       -3.110810e-26])

print(start - gc.mem_free())

 

#@timed_function
def its90_K(E):

    Ev = E 
    T= 0.0
    
    if E > 20644: #20,644 to 54,886 μV (500 -1373 C)
        T = _CKi2[0]
        
        for i in range(1,7):
            T+= _CKi2[i]*Ev
            Ev*= E
     
    elif E <= 0.:
         T = _CKi0[0]
         for i in range(1,9):
            T+=_CKi0[i]*Ev 
            Ev*=E
        
    else: # 0 μV to 20644 μV  (0-500 C)

        T =_CKi1[0]
        #Ev = E
        for i in range(1,8):
            T+= _CKi1[i]*Ev 
            Ev*=E
        T+= _CKi1[8]*Ev    
        a = _CKi1[9]*Ev
        a*= E
        T+=a
    
    return T

# if __name__ == '__main__':

    
#     E=[-6458,-3852 ,397 ,1000,10153,20644,22990,24905,27658,32041,32289,37725,48838,54886] # [uV]
#     Tref = [-270,- 110,10, 25,250,500,555, 600, 665, 770,776, 910,1200,1372] # [C]
#     
#     for i in range(len(E)):
#         T= its90_K(E[i])
#         print(Tref[i])
#         
#         