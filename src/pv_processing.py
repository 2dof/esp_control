# MicroPython p-i-d-isa library
#The MIT License (MIT), Copyright (c) 2022-2023 L.Szydlowski
##https://github.com/2dof/esp_control
# __version__   = "1.0.0"

import uctypes
from uctypes import BF_POS, BF_LEN, BFUINT8,UINT8, UINT16 ,FLOAT32, UINT32, BFUINT32

from math import fabs, sqrt
from utils_pid_esp32 import deadband, limit

from benchmark import timed_function
 
# PV 
PV_FIELDS = {
    "Pvisel":    0<<BF_POS | 1<<BF_LEN | BFUINT8,  
    "Sqrtsel":   1<<BF_POS | 1<<BF_LEN | BFUINT8,  
    "Fltsel":    2<<BF_POS | 1<<BF_LEN | BFUINT8,  
    "f3":        3<<BF_POS | 1<<BF_LEN | BFUINT8,  
    "f4":        4<<BF_POS | 1<<BF_LEN | BFUINT8,
    "f5":        5<<BF_POS | 1<<BF_LEN | BFUINT8,
    "F6":        6<<BF_POS | 1<<BF_LEN | BFUINT8,
    "F7":        7<<BF_POS | 1<<BF_LEN | BFUINT8,    
    }

PV_REGS = {              # 72 bytes
    "PvLL":   0x00|FLOAT32,   
    "PvHL":   0x04|FLOAT32,   
    "PvaL":   0x08|FLOAT32,    
    "PvaH":   0x0C|FLOAT32,   
    "PvbL":   0x10|FLOAT32,   
    "PvbH":   0x14|FLOAT32,   
    "SqrtbL": 0x18|FLOAT32,    
    "SqrtbH": 0x1C|FLOAT32,   
    "Ts":     0x20|FLOAT32,   
    "Tf":     0x24|FLOAT32,    
    "pv":     0x28|FLOAT32,   
    "yf":     0x2C|FLOAT32,   
    "sclin":  0x30|FLOAT32,   
    "scsqrt": 0x34|FLOAT32,     
    "CFG_REG":0x38|UINT8,     
    "CFG":    (0x38,PV_FIELDS) 
    }

 
#---pv processing---------------
def pv_update(pvr,pve,pvi = 0.0):
    
    pvr.pv = pve
    
    if pvr.CFG.Pvisel: 
        pvr.pv = pvi
 
    pvr.pv = (pvr.pv-pvr.PvaL)*pvr.sclin + pvr.PvbL     
 
    if pvr.CFG.Fltsel:
        pvr.pv = lp_filter(pvr.pv, pvr.yf, pvr.Ts,pvr.Tf)
        pvr.yf= pvr.pv
      
    if pvr.CFG.Sqrtsel:
        print(pvr.pv)
        pvr.pv =pvr.scsqrt*sqrt(pvr.pv)+pvr.SqrtbL  
         
    return pvr.pv


def pv_tune(pvr):
    pvr.sclin = (pvr.PvbH-pvr.PvbL)/(pvr.PvaH-pvr.PvaL)
    pvr.scsqrt = (pvr.SqrtbH-pvr.SqrtbL)/10
    
    
def pv_reset(pvr):
    pvr.yf = 0.0

def pv_init0(pvr):
    pvr.PvLL = 0.0
    pvr.PvHL = 100.   
    pvr.PvaL = 0.0  
    pvr.PvaH = 100.  
    pvr.PvbL = 0.0 
    pvr.PvbH = 100.  
    pvr.SqrtbL =  0.
    pvr.SqrtbH =  10.
    pvr.Ts = 0.1     
    pvr.Tf = 0.5* pvr.Ts  
    pvr.pv = 0.0    
    pvr.yf = 0.0    
    pvr.sclin  = (pvr.PvbH-pvr.PvbL)/(pvr.PvaH-pvr.PvaL)
    pvr.scsqrt = (pvr.SqrtbH-pvr.SqrtbL)/10
    

#-----------------------------------------------
if __name__ == '__main__':
    pass
    
 

