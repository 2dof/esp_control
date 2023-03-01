# MicroPython p-i-d library
#https://github.com/2dof/esp_control
#The MIT License (MIT), Copyright (c) 2022-2023 L.Szydlowski
# __version__   = "1.0.0"
 

import uctypes
from uctypes import BF_POS, BF_LEN, BFUINT8,UINT8, UINT16 ,FLOAT32, UINT32, BFUINT32

from math import fabs, sqrt
from utils_pid_esp32 import deadband, limit


SP_FIELDS = {
    "SPesel":    0<<BF_POS | 1<<BF_LEN | BFUINT8, #  
    "Rlimsel":   1<<BF_POS | 1<<BF_LEN | BFUINT8, #  
    "SPgen":     2<<BF_POS | 1<<BF_LEN | BFUINT8, #  
    "f3":        3<<BF_POS | 1<<BF_LEN | BFUINT8,  
    "f4":        4<<BF_POS | 1<<BF_LEN | BFUINT8,
    "f5":        5<<BF_POS | 1<<BF_LEN | BFUINT8,
    "F6":        6<<BF_POS | 1<<BF_LEN | BFUINT8,
    "F7":        7<<BF_POS | 1<<BF_LEN | BFUINT8,    
    }

SP_REGS = {
    "SpLL":   0x00|FLOAT32,   
    "SpHL":   0x04|FLOAT32,  
    "SpeaL":  0x08|FLOAT32,   
    "SpeaH":  0x0C|FLOAT32,  
    "SpebL":  0x10|FLOAT32,   
    "SpebH":  0x14|FLOAT32,  
    "Rlim":   0x18|FLOAT32,   
    "Ts":     0x1C|FLOAT32,   
    "sp":     0x20|FLOAT32,   
    "sclin":  0x24|FLOAT32,  
    "sp1":    0x28|FLOAT32,   
    "dx":     0x2C|FLOAT32,  
    "CFG_REG":0x30|UINT8,
    "CFG":    (0x30,SP_FIELDS)
    }


def sp_update(spr,spi,spe = 0.0):
    
    spr.sp = spi
    
    if spr.CFG.SPesel: 
        spr.sp = (spe-spr.SpeaL)*spr.sclin + spr.SpebL
    
    spr.dx = spr.sp-spr.sp1
    
    if spr.CFG.Rlimsel:
       
        delta = spr.Rlim * spr.Ts

        if (fabs(spr.dx)>(delta)):
           if (spr.dx<0):
               delta *= -1
           spr.dx = delta 
           spr.sp = spr.sp1+delta
    
    spr.sp = limit(spr.sp,spr.SpLL,spr.SpHL)
    spr.sp1= spr.sp
    
    return spr.sp 

def sp_tune(spr):
    spr.sclin = (spr.SpebH-spr.SpebL)/(spr.SpeaH-spr.SpeaL)

def sp_reset(spr):
    spr.sp1 = 0.0 
    spr.dx  = 0.0

def sp_init0(spr):
    spr.SpLL   =0.
    spr.SpHL  =100
    spr.SpeaL  = 0. 
    spr.SpeaH  = 100
    spr.SpebL  = 0.
    spr.SpebH  = 100.
    spr.Ts     = 0.1
    spr.Rlim   =1.
    spr.sclin  = (spr.SpebH-spr.SpebL)/(spr.SpeaH-spr.SpeaL)  
    spr.sp1    = 0.0 
    spr.dx     = 0.0 
    spr.CFG.SPesel =True
    
  