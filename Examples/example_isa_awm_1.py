#The MIT License (MIT), Copyright (c) 2022-2023 L.Szydlowski
#https://github.com/2dof/esp_control
#

from pid_isa import *
from mv_processing import *
from simple_models import FOPDT_model

from random import uniform 

# simulation time init 
Tstop=20
Ts =  0.1 
Ns=int(Tstop/Ts)

#[1] process model FOPDT


model = FOPDT_model(Kp=2.0,taup=3.0,delay=1.0, y0=0.0,Ts=Ts)

#[2] PID Controller initialization 
pid_buf=bytearray(128)  # size of ISA_REGS is 128 bytes, 
PID = uctypes.struct(uctypes.addressof(pid_buf), ISA_REGS, uctypes.LITTLE_ENDIAN)
isa_init0(PID)  
    

#[3] Manual Value  initialization
mv_buf=bytearray(41)   
MVR = uctypes.struct(uctypes.addressof(mv_buf), MV_REGS, uctypes.LITTLE_ENDIAN)
mv_init0(MVR)

MVR.Ts = Ts 
MVR.MvHL = 0.95* PID.Umax   # we seta limits as 95% of Umax and 5% if umin
MVR.MvLL = 0.95* PID.Umin
mv_tune(MVR)


#4 - pid tuning 
# we assume that we know process params calculated from proces step responce 
# see https://yilinmo.github.io/EE3011/Lec9.html#org2a34bd4

Ko = 2  # -> Kp         
To = 3.   #  -> taup 
Lo = 1.   #  -> delay

# calculate The PID parameters from Ziegler-Nichols Rules
# PID.Ts = Ts
# PID.Kp = 1.2*To/(Ko*Lo)
# PID.Ti = 2*Lo
# PID.Td = 0.5*Lo
# PID.Tm = PID.Td/10.

  #Tuning based on IMC (internal Model Control) for 2-dof pid (see D action calculation comment:(!))  
    #tauc = max(1*Ko, 8*Lo)      #  'moderate' tutning
tauc = max(1*To, 1*Lo)  #  'agressive' tuning 
PID.Kp   =((To+0.5*Lo)/(tauc+0.5*Lo))#/Ko
PID.Ti   =(To+0.5*Lo)
PID.Td   = To*Lo/(2*To+Lo)
PID.Tm   = PID.Td/10.

isa_tune(PID)     # P-I-I secetect 

PID.CFG.Awsel   = False  # True
PID.CFG.Dsel   = True  # True


# init simulation 
sp = 50.     # setpoint
yk  = 0.      # proces outpout value (measured)
uk  = 0.      # control value 
dmv = 0.     # change in manual value
mv  = 0.     # manual value 
utr = uk

for i in range(Ns):
    #[a] Read process value (in real time wee read from ADC and do pv processing)
    yk = model.update(uk)
    #vn = uniform(-0.4,0.4)  # white noise  
    pv = yk #+ vn
    
    # [b]update setpoint (in real solution we do some sp processing)
    sp=50
    if i >=100:
       sp = -50

#     #[c] update mv processing
    mv = mv_update(MVR,dmv,uk)
#     
#     #[d] update control pid,
    u = isa_updateControl(PID,sp , pv, utr,ubias = 0.)  
# 
#     # [e]We are in AUTO mode (PID.CFG.Mansel=False) so we do not mv this time. 
    if PID.CFG.Mansel:       
         u = mv           # we get manual value    
#    
#     # [f] saturation checking
    uk = limit(u, PID.Umin,PID.Umax)
#     
    utr = uk    #  do not forget update tracking
    
    #[g] in real time do some control value processing we sent uk to DAC,and wait Ts
  
    print("sp:",sp,"pv:",pv,"uk:",uk)
     
    

