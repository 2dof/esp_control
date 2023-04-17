

## Contents
 1. [Example 1: PID-ISA with anti-windup](#1-pid-isa-with-anti-windup)  
 2. [Example 2: Class controller example - implementing OOP tutorial](#2-class-controller-example )  
 


 
 

# 1. PID-ISA with anti-windup 

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
  


# 2. Class controller example  

This tutorial will cover:
- Part 1: Implementing basic  p-i-d controller as class object  
- Part 2: Using timer interrupt (esp32 micropython) 

Tutorial will not cover how to implement fully application (menu system, loading data from memory) but some sugestions will be added in part 2

In this example, a ```pid_awm_updateControl()``` function from pid_aw.py will be used as the main p-i-d algorithm, and a FOPDT_model (from simple_models_esp.py) will be used for simulation.

**introduction**

A basic sequence in digital (discrete) p-i-d implementation is ("PID Controllers - Theory, Design and Tuning" by Karl J. Aström and Tore Hägglund, sec. 3.6 Digital Implementation).

(1) Wait for clock interrupt.
(2) Read analog input  (Process value, (Setpoint)). 
(3) Compute control signal.
(4) Set analog output ( before do some preprocessing) 
(5) Update controller variables 
(6) Go to 1 

From above, we can notice that step (5) is done after setting physical output (the control value (Cv) should be calculated and updated as fast as possible), which means that the controller's parameters and variables can't be modified during Cv calculations (to avoid unexpected behavior). Because p-i-d parameters: Kp, Ti, Td, Tm, Td, Umax, Umin, dUlim and Ts (see  [2.2 PID with anti-windup](https://github.com/2dof/esp_control/#22-pid-with-anti-windup) for full structure description) can be changed at any time by the user, we need a copy of parameters, and that functionality will be implemented in Part 1 of the tutorial. 

In step (2) some additional signal processing (at least unit conversion) is needed, and the setpoint (Sp) can be set by a potentiometer, so noise filtering may be necessary. In hardware solution, at least Sp, Pv, error, Cv  should be presented on display, and for Sp value setting (user->Sp setting (with potentiometer)-display->user), the frequency of the display update can differ from the p-i-d sampling time (especially when we control a slow process, a Cv can be calculated even every few seconds); in that case, a user menu system (for the keyboard and display) should take care of Sp noise filtration).
In step (4), we usually set a PWM output as an analog output, but it can also be  PWM + DO (digital output) (ffor DC motor control with direction), or just DO (On-off control).

**Part 1: P-I-D Class** 

The code for the pid_awm_controller() class is presented below. As a basic, we have:
- pid structure, descibed in [2.2 PID with anti-windup](https://github.com/2dof/esp_control/#22-pid-with-anti-windup))
- local copy of parameters Kp,Ti,Td,Tm, Td, Umax,Umin, dUlim, Ts 
- flag ``` Fparam ``` for informing if parameters has been change and recalculation will be nedeed 

As additional to Cv calculation a rate limiter has beed added in  updateControl() function. By setting parametes with function ```set_<parameter>(value)``` we set 
 local parameter and set ``` Fparam ``` flag, but only function ``` tune() ``` will recalculate all variables and will update p-i-d structure ```self.pid ```
 
file class_controller_pid_awm_example.py (with simulation in ```__main__```): 
```
class pid_awm_controller(object):    __init__(self,Kp,Ti,Td,Tm,Tt,Umax=100,Umin =0 ,dUlim=100,Ts = 1.0) 
    ├──                                   
    ├── updateControl(self,sp,pv,ubias=0.,mv=0.)         
    ├── tune()                                   - recalculate p-i-d variables        
    ├── set_Kp(value)                            - set local Kp parameter.
    ├── set_Ti(value)                            - set local Ti parameter
    ├── set_Td(value)                                 
    ├── set_Tm(value)
    ├── set_Tt(value)      
    ├── set_Umax(value)   
    ├── set_Umin(value)   
    ├── set_dUlim(value)       
    └── set_Ts(value)                            - set local Ts paramwter
```

This way we created a basic pid 'block' where we can set parameters in any time, and update controller's variable later. 
Note that:
- in ```set_<parameter>(value)``` functions, value error checking hasn't beed added.  
-  when we analyze source code of pid_awm_updateControl() function, we notice that computation of variables are done in 
  pid_tune(pid) function, and only parameter Kp is used directly in P-term calculation in ```pid_awm_updateControl()```. That mean a most of parameter (Ti,Td,..) apart from Kp can be changed directrly in struct without affecting Cv calculation, so class can be optimized (not need to keep coopy of (Ti,Td,..), but for consistency we keep all parameters as auxiliary values.  
 
 

class pid_awm_controller() implementation: 
```python 
from pid_aw import *  

class pid_awm_controller(object):
    def __init__(self,Kp,Ti,Td,Tm,Tt,Umax=100,Umin =0 ,dUlim=100,Ts = 1.0):

        self.pid_buf=bytearray(101)  # size of PID_REGS is 101 bytes, 
        self.pid = uctypes.struct(uctypes.addressof(self.pid_buf), PID_REGS, uctypes.LITTLE_ENDIAN)
        
        self.Kp = Kp      
        self.Ti = Ti        
        self.Td = Td        
        self.Tm = Tm       
        self.Tt = Tt           
        self.Umax = Umax     
        self.Umin = Umin       
        self.dUlim = dUlim    
        self.Ts    =  Ts  
        
        self.tune()   
         
        self.Fparam=False   
        
        self.pid.CFG.Psel = True
        self.pid.CFG.Isel = True
        self.pid.CFG.Dsel = False
       
    def updateControl(self,sp,pv,ubias=0.,mv=0.):
        
        uk = pid_awm_updateControl(self.pid,sp,pv,ubias,mv)
        
        if self.pid.CFG.Rlimsel: 
           
           delta=self.pis.dUlim * PID.Ts
           du=self.pid.u-self.pid.u1
           
           if (abs(du)>delta):    
               if (du<0):
                   delta *=-1
               
               du = delta 
               self.pid.u=self.pid.u1+du
               uk= self.pid.u
        
        return uk
       
    def tune(self): 
        
        self.pid.Kp = self.Kp
        self.pid.Ti = self.Ti  
        self.pid.Td = self.Td  
        self.pid.Tm = self.Tm 
        self.pid.Tt = self.Tt
        self.pid.Ts = self.Ts    
        self.pid.Umax = self.Umax 
        self.pid.Umin = self.Umin   
        self.pid.dUlim= self.dUlim
        
        pid_tune(self.pid)
        self.Fparam =False
            
    def set_Kp(self,value):
        self.Kp = value
        self.Fparam =True
 
    def set_Ti(self,value):  
        self.Ti = value
        self.Fparam =True
        
    def set_Td(self,value):
        self.Td = value
        self.Fparam =True
        
    def set_Tm(self,value):
        self.Tm = value
        self.Fparam =True
        
    def set_Ts(self,value):
        self.Ts    = value
        self.Fparam =True
        
    def set_Tm(self,value):
        self.Tt = value
        self.Fparam =True
        
    def set_Umax(self,value):
        self.Umax  = value
        self.Fparam =True
        
    def set_Umin(self,value):
        self.Umin  = value
        self.Fparam =True
        
    def set_dUlim(self,value):
        self.dUlim = value
        self.Fparam =True

```

**Simulation** 

As simulation example we control a FOPDT (first order Process with delay time) as a very simple thermal process. Let's assume that we controll some boiler with SSR as actuator with continuous control (by PWM : 0% to 100 % ), and we measure proces value as °C.  
As a basic PID configuration we use:
- P-I controller
- Control Mode: normal (controller.pid.CFG.Rlimsel = False  -> error = sp - pv)
- Rate limiter off ( controller.pid.CFG.Rlimsel=False)
- Control limit Umin =0.0  

We change setpoint during simulation from 50 °C  to 30 °C and then to 60 °C. As a result of simulation we get signals presented on waveforms (during simulation results will be printed): 

<img src="https://github.com/2dof/esp_control/blob/main/Examples/drawnings/pid_awm_class_p1_neg.png" width="700" height="300" />

The upper waveforms show the setpoint (sp) and process value (pv), the lower control value output (u), and the control value (uk) before limiting [Umin, Umax] 
Let's notice that when changing the setpoint from 50 °C  do 30 °C the process temperature dynamics is much slower than when we increase Sp.  
Since the possible physical value for SSR PWM will be 0% (power off) the controller is unable to set Cv below the physical limit in the first 30 seconds the temperature will drop only with the speed of process dynamics (cooling). 

simlulation 'in the loop':
```
.... 
if __name__ == '__main__':

    from simple_models_esp import FOPDT_model
 
    # simulation time amd sampling
    Ts =.25
    Tstop= 50
    Ns   = int(Tstop/Ts)
 
    #[1] process model FOPDT
    y0=21      # Initial value 
    To=200     # proces time constant 
    Lo=1       # proces delay [s]
    Ko=100     # process Gain [s]
    process_model = FOPDT_model(Kp=Ko,taup=To,delay=Lo, y0=y0,Ts=Ts)

    # P-I controller settings
    Kp0 = 0.5 
    Ti0 = 10 
    Td0 =1.0 
    Tm0 = 0.25
    Tt0= Ts
    
    controller=pid_awm_controller(Kp=Kp0,Ti=Ti0,Td=Td0,Tm=Tm0,Tt=Tt0,Umax=100,Umin =0 ,dUlim=100,Ts =.25)
    
    controller.pid.CFG.Dsel = False 
    
    sp = 50
    pv = 0.0
    uk = 0.0
    
    for i in range(Ns):

        #[a]changing Setpoint  
        sp=50 #   
        if k*Ts >=150:
           sp = 30

        if k*Ts >=300:
           sp = 60
           
        #[a] Read process value (in real time wee read from ADC and do pv processing)
        yk = process_model.update(uk)
        #vn = uniform(-0.4,0.4)  # white noise  
        pv = yk #+ vn
    
        uk = controller.updatecontrol(sp,pv)  # dafault ubias=0, mv = 0
        
        print(i,"sp:",sp,"pv:",pv,"uk:",uk)
```



*Part2: timer interrupt* 

Before some examples solutions will be presented familiarize yourself with micropython timer interrupts in esp32 and 
[Writing interrupts handlers](https://docs.micropython.org/en/latest/reference/isr_rules.html)
Main conclusions:
- esp32 timers interrups are implemented as soft interrupts
- in general it is best to avoid using floats in ISR code 
- ISR cannot pass a bound method to a function
         
Also using ISR with uasyncio there are [some restrictions](https://github.com/peterhinch/micropython-async/blob/master/v3/docs/INTERRUPTS.md)


