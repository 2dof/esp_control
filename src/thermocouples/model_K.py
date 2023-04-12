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
             -1.9889266878e-17,
             -1.6322697486e-20])


def its90model_K(temp):

    T = 1
    E = 0.0
    if temp>0:
        E = _CK1[0]
        for i in range(1,10):
            T*=temp
            E+=T*_CK1[i]
            
          
        x=-0.0001183432*(temp-126.9686)**2
        x=118.5976*exp(x)
        E+=x
    else:
        E = _CK0[0]
        for i in range(1,11):
            T*=temp
            E+=T*_CK0[i]
            
    return E    # [uv]

if __name__ == '__main__':
# 
     Eref=[-6458,-6404,-3852,-1889,0,  397 ,1000,10153,20644,22990,24905,27658,32041,32289,37725,48838,54886] # [uV]
     T  = [-270.,-250, -110.,-50.0,0.0,10.0,25.0,250.0,500.0,555.0,600.0,665.0,770.0,776.0,910.0,1200.,1372.] # [C]
#     
     for i in range(len(Eref)):
         Ei = its90model_K(T[i])
         print(i,Eref[i],Ei,' err:',Eref[i]-Ei)
 
