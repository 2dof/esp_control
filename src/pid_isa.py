# MicroPython p-i-d-isa library
#https://github.com/2dof/esp_control
#The MIT License (MIT), Copyright (c) 2022-2023 L.Szydlowski
# __version__   = "1.0.0"

import uctypes
from uctypes import BF_POS, BF_LEN, BFUINT8,UINT8,FLOAT32

from math import fabs, sqrt
from utils_pid_esp32 import deadband, limit
 
# dict def of pid config and params fields 
ISA_FIELDS = {
    "Psel":    0<<BF_POS | 1<<BF_LEN | BFUINT8,
    "Isel":    1<<BF_POS | 1<<BF_LEN | BFUINT8,
    "Dsel":    2<<BF_POS | 1<<BF_LEN | BFUINT8,
    "Awsel":   3<<BF_POS | 1<<BF_LEN | BFUINT8,
    "Mansel":  4<<BF_POS | 1<<BF_LEN | BFUINT8,
    "Modesel": 5<<BF_POS | 1<<BF_LEN | BFUINT8,  # 0 direct, 1 - indirect
    "Deadsel": 6<<BF_POS | 1<<BF_LEN | BFUINT8,
    "Rlimsel": 7<<BF_POS | 1<<BF_LEN | BFUINT8,    
}

ISA_REGS = {
    "Kp":      0x00|FLOAT32,     
    "Ti":      0x04|FLOAT32,     
    "Td":      0x08|FLOAT32,     
    "Tm":      0x0C|FLOAT32,     
    "Tt":      0x10|FLOAT32,     
    "b":       0x14|FLOAT32,     
    "c":       0x18|FLOAT32,     
    "Umax":    0x1C|FLOAT32,     
    "Umin":    0x20|FLOAT32,     
    "dUlim":   0x24|FLOAT32,     
    "Ts":      0x28|FLOAT32,     
    "Deadb":   0x2C|FLOAT32,     
    "Pk":      0x30|FLOAT32,     
    "Ik":      0x34|FLOAT32,     
    "Dk":      0x38|FLOAT32,        
    "Ki":      0x3C|FLOAT32,     
    "Kd":      0x40|FLOAT32,     
    "ai":      0x44|FLOAT32,     
    "bi":      0x48|FLOAT32,     
    "ad":      0x4C|FLOAT32,       
    "bd":      0x50|FLOAT32,     
    "ek":      0x54|FLOAT32,     
    "ed":      0x58|FLOAT32,
    "ep":      0x6C|FLOAT32,
    "du":      0x60|FLOAT32,
    "u":       0x64|FLOAT32,
    "ed1":     0x68|FLOAT32,    
    "u1":      0x7C|FLOAT32,    
    "CFG_REG": 0x70|UINT8,
    "CFG":    (0x70,ISA_FIELDS)
}
 
def isa_tune(pid):
    
    pid.Ki =pid.Kp /pid.Ti
    pid.Kd =pid.Kp * pid.Td
    pid.ai =pid.Ki * pid.Ts
    pid.bi =pid.Ts / pid.Tt
    pid.ad =(2*pid.Tm-pid.Ts)/(2*pid.Tm+pid.Ts)
    pid.bd =2*pid.Kd/(2*pid.Tm+pid.Ts)

def isa_reset(pid):
    pid.Ik  = 0.
    pid.Dk  = 0.
    pid.u   = 0.
    pid.u1  = 0.
    pid.ed1 = 0.
    
    
def isa_updateControl(pid,sp,pv,utr = 0.,ubias = 0.):
    
    pid.ek = sp - pv           
    pid.ed = pid.b*sp-pv     
    pid.ep = pid.c*sp-pv     
        
    if pid.CFG.Modesel:
        pid.ek *= -1         
        pid.ed *= -1      
        pid.ep *= -1
        
    if pid.CFG.Deadsel:
 
        pid.ek = deadband(pid.ek,pid.Deadb)
        pid.ed = deadband(pid.ed,pid.Deadb)
        pid.ep = deadband(pid.ep,pid.Deadb)
        
    pid.Pk = 0.    
        
    if pid.CFG.Psel:
        pid.Pk = pid.Kp * pid.ep
        
    if pid.CFG.Isel:
        pid.Ik +=pid.ai * pid.ek 
       
        if pid.CFG.Awsel:
            pid.Ik += pid.bi * (utr-pid.u)
    else:
        pid.Ik = 0.
        
    if pid.CFG.Dsel:
        pid.Dk=pid.Dk*pid.ad + pid.bd*(pid.ed-pid.ed1) 
    else:
        pid.Dk = 0.
        
    pid.u1 = pid.u  
    pid.u  = pid.Pk + pid.Ik + pid.Dk + ubias    
    pid.du = pid.u-pid.u1
    
    if pid.CFG.Rlimsel:
   
        delta=pid.dUlim * pid.Ts

        if (fabs(pid.du)>(delta)):
           if (pid.du<0):
               delta *=-1
           pid.du = delta 
           pid.u=pid.u1+delta
           
    pid.ed1 = pid.ed
    pid.u1  = pid.u
    
    return pid.u
     
def isa_init0(pid):
    # for step responce test
    pid.Kp = 1 
    pid.Ti = 1
    pid.Td = 1
    pid.Tm = 0.1 
    pid.Tt = 1 
    pid.b  = 1 
    pid.c  = 1
    pid.Umax = 100
    pid.Umin = -100
    pid.dUlim =100
    pid.Ts    =.1
    pid.Deadb = 0.1
    pid.Ik  = 0.
    pid.Dk  = 0.
    pid.u   = 0.
    pid.du  = 0.
    pid.u1  = 0.
    pid.ed1 = 0.0
    pid.CFG_REG =0x07  # Psel,Isel,Dsel = True
     
 
 
 
     