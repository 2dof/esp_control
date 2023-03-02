# MicroPython p-i-d-isa library
#The MIT License (MIT), Copyright (c) 2022-2023 L.Szydlowski
#
# __version__   = "1.0.0"

import uctypes
from uctypes import FLOAT32

from math import fabs, sqrt
from utils_pid_esp32 import limit
 
# MV   10*4=bytes
MV_REGS = {
    "MvLL":      0x00|FLOAT32,     
    "MvHL":      0x04|FLOAT32,     
    "Tt":        0x08|FLOAT32,     
    "Tm":        0x0C|FLOAT32,     
    "Ts":        0x10|FLOAT32,     
    "mvi":       0x14|FLOAT32, 
    "mvo":       0x18|FLOAT32,
    "at" :       0x1C|FLOAT32,
    "bt" :       0x20|FLOAT32,
    "ct" :       0x24|FLOAT32
    }

def mv_update(mvr,dmv,tr =0.0):
    
    mvr.mvi = mvr.mvi*mvr.at + dmv*mvr.bt + tr*mvr.ct  # tracking input tr

    mvr.mvo = limit(mvr.mvi ,mvr.MvLL,mvr.MvHL)
    
    return mvr.mvo


def mv_tune(mvr):
     # tracking block param update
     mvr.at=mvr.Tt/(mvr.Tt+mvr.Ts) 
     mvr.bt=(mvr.Tt*mvr.Ts)/(mvr.Tm*(mvr.Tt+mvr.Ts))  
     mvr.ct= mvr.Ts/(mvr.Tt+mvr.Ts)
    
def mv_reset(mvr):
    mvr.mvi = 0.0

def mv_init0(mvr):

    mvr.MvLL =-100.           
    mvr.MvHL =100
    mvr.Ts   =1.0
    mvr.Tt   =.5     #       
    mvr.Tm   =1.           
    mvr.mvi  =0.        
    mvr.mvo  =0.        
    mv_tune(mvr)       
     
 
 
    
    

