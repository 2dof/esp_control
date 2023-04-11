

**Example 1: PID-ISA with anti-windup** 

In this example we show how to implement a anti-windup scheme for pid-isa controller (see block diagram below), 
 we will use manual value (MV) processing  with Man/Auto switch to show how MV processing will be tracking a control value (CV). 

<img src="https://github.com/2dof/esp_control/blob/main/Examples/drawnings/pid_isa_awm_1_neg.png" width="300" height="230" />

Simulation will be done "in the loop" with First Order Process with Delay Time (FOPDT) as controlled process.

Whole code: example_isa_awm_1.py

First, import pid control, manual value processing functions and process model from ```simple_models_esp.py```, We set simulation time and 
define sampling time as Ts =0.1.

```python
from pid_isa import *
from mv_processing import *
from simple_models_esp import FOPDT_model

from random import uniform 

# simulation time init 
Tstop=20
Ts =  0.1 
Ns=int(Tstop/Ts)
```

We create FOPDT process model with delay 1 sec, proces time constant taup=3.0 sec, and process gain Kp=2, next 
we initialize a P-I-D controller and (PID structure) and Manual Value MVR structure, We set 
MvHL ,MvLL slightly smaller than control Umin/Umax.

``` Python
#[1] process model FOPDT
process_model = FOPDT_model(Kp=2.0,taup=3.0,delay=1.0, y0=0.0,Ts=Ts)

#[2] PID Controller initialization 
pid_buf=bytearray(128)  # size of ISA_REGS is 128 bytes, 
PID = uctypes.struct(uctypes.addressof(pid_buf), ISA_REGS, uctypes.LITTLE_ENDIAN)
isa_init0(PID)  
    
#[3] Manual Value  initialization
mv_buf=bytearray(41)   
MVR = uctypes.struct(uctypes.addressof(mv_buf), MV_REGS, uctypes.LITTLE_ENDIAN)
mv_init0(MVR)

MVR.Ts = Ts 
MVR.MvHL = 0.95* PID.Umax   # we seta limits as 95% of Umax andUmin
MVR.MvLL = 0.95* PID.Umin
mv_tune(MVR)
```

Next we perform a PID tuning, as example two method are presented: a standard step responce (Ziegler-Nichols method) and  
tuning based on IMC (internal Model Control) , note that IMC is for 2-dof controller (i.e D-action is calculated not for
error = sp - pv but for -y value - we use standard error = sp - pv for D-calculation). 
After calling ```isa_tune(PID)``` we set selectors for anti-windup (Awsel) and PI/PID select control - We will change selectors
for testing our setup.  

``` Python
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

  #Tuning based on IMC (internal Model Control) for 2-dof pid  
 #tauc = max(1*Ko, 8*Lo)      #  'moderate' tutning
tauc = max(1*To, 1*Lo)  #  'agressive' tuning 
PID.Kp   =((To+0.5*Lo)/(tauc+0.5*Lo))#/Ko. 
PID.Ti   =(To+0.5*Lo)
PID.Td   = To*Lo/(2*To+Lo)
PID.Tm   = PID.Td/10.

isa_tune(PID)     # P-I-I secetect 

PID.CFG.Awsel   = False  # True
PID.CFG.Dsel   = True  # True
```
Because we simulate control in the loop we:
- initialize parameters, setpoint sp = 50 (we change in middle of the iteration to sp=-50 
- initialize other parameters.

a) - read value yk from process model and simulate a measurement ```pv = yk + vn```,(vn- noise), for first test we do not add noise.
b) - set sp value and change during simulation
c) - update manual value processing ( we will just use to show tracking functionality)
d) - update control value, because pid-isa (isa_updateControl()) has not implemented Man/Auto switch (but PID structure has selector) we 
      add selector Man/Auto
e) in Manual mode (Mansel =True) we just overwrite output control value form ```isa_updateControl()```  with manual value mv (We will not use 
   switch Man/Auto in this example)
f) - we call ```limit()``` function to limit control signal, and we feed-up output uk control signal to tracking input utr in ```isa_updateControl()``` function,
    when PID.CFG.Awsel = True the anti-windup (with back calculation) will be active.
g) last step is just to print signals.

```python
# init simulation 
sp = 50.     # setpoint
yk  = 0.      # proces outpout value (measured)
uk  = 0.      # control value 
dmv = 0.     # change in manual value
mv  = 0.     # manual value 
utr = uk

for i in range(Ns):
    #[a] Read process value (in real time wee read from ADC and do pv processing)
    yk = process_model.update(uk)
    #vn = uniform(-0.4,0.4)  # white noise  
    pv = yk #+ vn
    
    # [b]update setpoint (in real solution we do some sp processing)
    sp=50
    if i >=100:
       sp = -50

#     #[c] update mv processing
    mv = mv_update(MVR,dmv,uk)
 
#  #[d] update control pid,
    u = isa_updateControl(PID,sp , pv, utr,ubias = 0.)  
 
#   # [e]We are in AUTO mode (PID.CFG.Mansel=False) so we do not mv this time. 
    if PID.CFG.Mansel:       
         u = mv           # we get manual value    
  
#   # [f] saturation checking
    uk = limit(u, PID.Umin,PID.Umax)
    
    utr = uk    #  do not forget update tracking
    
    #[g] in real time do some control value processing we sent uk to DAC,and wait Ts
  
    print("sp:",sp,"pv:",pv,"uk:",uk,'mv:',mv)
     
```
Below printed data are presented on plots for easier analysis. Figure 1. present process control without
anti-windup, the second with antntiwindup active. 
On the bottom chart we can see how manual value (mv) track a control signal to ensure bumpless swiching from Auto to Manual control mode.  

  <table style="padding:4px">
  <tr>
     <td> <img src="https://github.com/2dof/esp_control/blob/main/Examples/drawnings/isa_awsel0_neg.png" width="450" height="250" /> 
     <br><p align="center">  figure 1.0.  Anti-windup Off</center><br> 
  
 </p></td>
     <td> <img src="https://github.com/2dof/esp_control/blob/main/Examples/drawnings/isa_awsel1_neg.png" width="450" height="250" />  
      <br><p align="center"> figure 1.1.  Anti-windup ON</center><br> 
  
 </p></td>
  </tr> </table> 
  
 In real time implementation all signal processing ( from reading process, value to control calcupation) shoud be implemented as 
 timer interrupt callback function, all parameters update and tuning shoud be done after end of control process update. 
  



*Example 2: Class controller example -  implementing OOP tutorial* 

This tutorial will cover:
- Part 1: implementing basic  p-i-d controller as class object  
- Part2 : using timer interrupt as hardware implementation of controller (esp32) 

Tutorial will not cover how to implement fully application (fully functional controller) but some sugestions will be added) 

In thos example a  ```  pid_aw_updateControl() ``` form pid_aw.py will be use as main p-i-d alghorithm and for simulation purpose a FOPDT_model ( from simple_models_esp.py

**introduction**

A basic sequence in digital (discrete) p-i-d implementation is ("PID Controllers - Theory Design and Tuning" by Karl J. Aström and Tore Hägglund, sec. 3.6 digital implementation):
(1) Wait for clock interrupt
(2) Read analog input  (Process value, Setpoint)    
(3) Compute control signal
(4) Set analog output 
(5) Update controller variables
(6) Go to 1 

From above, we can notice that step (5) is done after setting physical output (the control value (Cv) should be calculated and updated as fast as possible), which means that the controller's parameters and variables can't be modified during Cv caluations (to avoid unexpected behavior). Because p-i-d parameters: Kp, Ti, Td, Tm, Td, Umax, Umin, dUlim and Ts (see      





