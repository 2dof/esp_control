# MicroPython p-i-d-isa library
#The MIT License (MIT), Copyright (c) 2022-2023 L.Szydlowski
# __version__   = "1.0.0"
##https://github.com/2dof/esp_control

import uctypes
from uctypes import BF_POS, BF_LEN, BFUINT8,UINT8  ,FLOAT32,   
from utils_pid_esp32 import deadband, limit



# dictionary
PID_FIELDS = {
    "Psel":    0<<BF_POS | 1<<BF_LEN | BFUINT8,
    "Isel":    1<<BF_POS | 1<<BF_LEN | BFUINT8,
    "Dsel":    2<<BF_POS | 1<<BF_LEN | BFUINT8,
    "Mansel":  3<<BF_POS | 1<<BF_LEN | BFUINT8,
    "Modesel": 4<<BF_POS | 1<<BF_LEN | BFUINT8,  # 0 direct, 1 - indirect
    "Rlimsel": 5<<BF_POS | 1<<BF_LEN | BFUINT8,
    "F6":      6<<BF_POS | 1<<BF_LEN | BFUINT8,
    "F7":      7<<BF_POS | 1<<BF_LEN | BFUINT8,
}
PID_REGS = {
    "Kp":      0x00|FLOAT32,     
    "Ti":      0x04|FLOAT32,     
    "Td":      0x08|FLOAT32,     
    "Tm":      0x0C|FLOAT32,     
    "Tt":      0x10|FLOAT32,      
    "Umax":    0x14|FLOAT32,    
    "Umin":    0x18|FLOAT32,      
    "dUlim":   0x1C|FLOAT32,     
    "Ts":      0x20|FLOAT32,     
    "Pk":      0x24|FLOAT32,      
    "Ik":      0x28|FLOAT32,     
    "Dk":      0x2C|FLOAT32,        
    "Ki":      0x30|FLOAT32,     
    "Kd":      0x34|FLOAT32,     
    "ai":      0x38|FLOAT32,        
    "bi":      0x3C|FLOAT32,     
    "ad":      0x40|FLOAT32,     
    "bd":      0x44|FLOAT32,     
    "ek":      0x48|FLOAT32,     
    "u":       0x4C|FLOAT32,       
    "uk":      0x50|FLOAT32,     
    "ek1":     0x54|FLOAT32,     
    "u1":      0x58|FLOAT32,  
    "CFG_REG": 0x6C|UINT8,
    "CFG":    (0x6C,PID_FIELDS)
}




#@timed_function
def pid_aw_updateControl(pid, sp,pv ,ubias = 0.):
    
    pid.ek = sp - pv           
          
    if pid.CFG.Modesel:
        pid.ek *= -1         
        
    pid.Pk = 0.    
        
    if pid.CFG.Psel:
        pid.Pk = pid.Kp * pid.ek
        
    if pid.CFG.Isel:
        pid.Ik +=pid.ai * pid.ek
    else:
        pid.Ik = 0.
        
    if pid.CFG.Dsel:
        pid.Dk=pid.Dk*pid.ad + pid.bd*(pid.ek-pid.ek1) 
    else:
        pid.Dk = 0.
        
    pid.uk  = pid.Pk + pid.Ik + pid.Dk + ubias

    pid.u = limit(pid.uk, pid.Umin,pid.Umax)
     
    pid.Ik += pid.bi * (pid.u-pid.uk) # antiwindup  
        
    pid.ek1 = pid.ek
    pid.u1  = pid.u
    
    return pid.u


def pid_awm_updateControl(pid,sp,pv,ubias = 0.,mv = 0.):
    
    pid.ek = sp - pv           
          
    if pid.CFG.Modesel:
        pid.ek *= -1         
        
    pid.Pk = 0.    
        
    if pid.CFG.Psel:
        pid.Pk = pid.Kp * pid.ek
        
    if pid.CFG.Isel:
        pid.Ik +=pid.ai * pid.ek
    else:
        pid.Ik = 0.
        
    if pid.CFG.Dsel:
        pid.Dk=pid.Dk*pid.ad + pid.bd*(pid.ek-pid.ek1) 
    else:
        pid.Dk = 0.
        
    pid.uk  = pid.Pk + pid.Ik + pid.Dk + ubias
    
    if pid.CFG.Mansel:
        pid.u = limit( mv, pid.Umin,pid.Umax)
    else: 
        pid.u = limit(pid.uk, pid.Umin,pid.Umax)
     
    pid.Ik += pid.bi * (pid.u-pid.uk)  
        
    pid.ek1 = pid.ek
    pid.u1  = pid.u
    
    return pid.u

def pid_tune(pid):
    
    pid.Ki =pid.Kp /pid.Ti
    pid.Kd =pid.Kp * pid.Td
    pid.ai =pid.Ki * pid.Ts
    pid.bi =pid.Ts / pid.Tt
    pid.ad =pid.Tm/(pid.Tm+pid.Ts) 
    pid.bd =pid.Kd/(pid.Tm+pid.Ts)



def pid_init0(pid):
    # for step responce test
    pid.Kp = 1 
    pid.Ti = 1
    pid.Td = 1
    pid.Tm = pid.Td/10.
    pid.Tt = 0.1 
    pid.Umax = 100
    pid.Umin = -100
    pid.dUlim =100
    pid.Ts    =.1
    pid.Ik  = 0.
    pid.Dk  = 0.
    pid.u   = 0.
    pid.uk  = 0.
    pid.u1  = 0.
    pid.ek1 = 0.0
    pid.CFG_REG =0x07     # Psel,Isel,Dsel = True
    pid_tune(pid)


# if __name__ == '__main__':
#     
#     pid_buf=bytearray(101)  # size of PID_REGS is 101 bytes, 
#     PID1 = uctypes.struct(uctypes.addressof(pid_buf), PID_REGS, uctypes.LITTLE_ENDIAN)
#     pid_init0(PID1)
#     
#     PID1.Kp = 2
#     PID1.Tt = PID1.Ts # 0.1
#     pid_tune(PID1)
#     
#     # and test settings
#     PID1.CFG.Modesel = False # True
#      
#     # get step responce  of PID
#     sp =10.
#     pv=0.
#     for i in range(0,25):
#         #u = pid_aw_updateControl(PID1,sp,pv,ubias = 0.)
#         u = pid_awm_updateControl(PID1,sp,pv,ubias=0.,mv =0.)
#     
#         print("u:",u,"uk:",PID1.uk)
    
    