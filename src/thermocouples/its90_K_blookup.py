# https://github.com/2dof/esp_control
#The MIT License (MIT), Copyright (c) 2022-2023 L.Szydlowski
# __version__   = "1.0.0"


#import array
from lookup_search import bytes_search
from benchmark import timed_function

# -0....1370 , every 10 C 
_ITS90_EKB = b'\x00\x00\x8d\x01\x1d\x03\xb3\x04K\x06\xe7\x07\x84\t#\x0b\xc3\x0cb\x0e\x00\x10\x9c\x118\x13\xcf\x14g\x16\xfa\x17\x8c\x19\x1d\x1b\xac\x1c;\x1e\xca\x1f[!\xec"\x7f$\x13&\xa8\'A)\xda*v,\x13.\xb1/P1\xf02\x91426\xd57y9\x1d;\xc2<g>\r@\xb4A[C\x03E\xaaFTH\xfdI\xa6KPM\xfaN\xa4PNR\xf9S\xa4UNW\xf8X\xa3ZM\\\xf7]\xa0_Ia\xf2b\x9bdCf\xe9g\x91i7k\xddl\x81n&p\xc9qls\ru\xadvNx\xedy\x8c{(}\xc5~a\x80\xfb\x81\x95\x83-\x85\xc5\x86\\\x88\xf1\x89\x86\x8b\x19\x8d\xac\x8e=\x90\xce\x91]\x93\xec\x94z\x96\x06\x98\x92\x99\x1c\x9b\xa5\x9c.\x9e\xb5\x9f<\xa1\xc1\xa2E\xa4\xc8\xa5J\xa7\xcb\xa8K\xaa\xca\xabF\xad\xc4\xae?\xb0\xb9\xb11\xb3\xa8\xb4\x1f\xb6\x93\xb7\x07\xb9x\xba\xe9\xbbY\xbd\xc6\xbe2\xc0\x9d\xc1\x06\xc3n\xc4\xd4\xc58\xc7\x9b\xc8\xfc\xc9\\\xcb\xba\xcc\x16\xcer\xcf\xcb\xd0#\xd2z\xd3\xcf\xd4"\xd6'

#@timed_function
def its90_K_blookup(E,low=0, high=137):
    
    idx = bytes_search(_ITS90_EKB,low,high, E)
    
    if idx ==-1:
       idx =136
       if E < 0:
          idx=0
          
    i=2*idx
    v1=int.from_bytes(_ITS90_EKB[i:(i+2)], 'little') 
    a=10/(int.from_bytes(_ITS90_EKB[(i+2):(i+4)], 'little') -v1)
    y= a*(E-v1)+idx*10 
    
    return (y,idx)

# if __name__ == '__main__':
# 
#     E=[-6458,-3852 ,397 ,1000,10153,20644,22990,24905,27658,32041,32289,37725,48838, 54886] # [uV]
#     Tref = [-270,- 110,10, 25,250,500,555, 600, 665, 770,776, 910,1200,1372] # [C]
#     
#     for i in range(len(E)):
#         T,idx = its90_K_blookup(E[i])
#         print(T)