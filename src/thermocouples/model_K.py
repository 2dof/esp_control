# https://github.com/2dof/esp_control
#The MIT License (MIT), Copyright (c) 2022-2023 L.Szydlowski
# __version__   = "1.0.0"
 


 

import array
from math import exp
from micropython import const
#from benchmark import timed_function
# ITS-90: IEC-60584-1-2013.pdf
_CK1=array.array('f',[-1.7600413686e1,   
               3.8921204975e1,   
               1.8558770032e-2,   
              -9.9457592874e-5,   
               3.1840945719e-7,   
              -5.6072844889e-10,  
               5.6075059059e-13,  
              -3.2020720003e-16,   
               9.7151147152e-20,   
              -1.2104721275e-23])
         
  # co -270 to 0 st c 
_CK0=array.array('f',[0.0000,          
              3.9450128025e1,
              2.3622373598e-2,
             -3.2858906784e-4,
             -4.9904828777e-6,
             -6.7509059173e-8,
             -5.7410327428e-10,
             -3.1088872894e-12,
             -1.0451609365e-14,
              1.9889266878e-17,
             -1.6322697486e-20])
 
_a0 = const(1.185976e2) 
_a1 = const(0.0001183432)


def its90model_K(temp):

    T = temp
    E = 0.0
    if temp>0:
        E = _CK1[0]
        for i in range(1,10):
            E+=T*_CK1[i]
            T*=temp
            
        x=_a1*(temp-126.9686)**2
        x=_a0*exp(x)
        E+=x
    else:
        E = _CK0[0]
        for i in range(10):
            E+=T*_CK0[i]
            T*=temp
            
    return E    # [uv]