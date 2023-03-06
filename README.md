

# ESP32 MIKROPYTHON CONTROL LIB

P-I-D control library for esp32 Micropython 

:exclamation:
actually only this doc is public, code will be published later. ANY QUESTIONS ? ->  Send a message 

<p align="center"> <img src="https://github.com/2dof/esp_control/blob/main/drawnings/PID_diagram_neg.png" width="700" height="300" />
<br> figure A0.</p>


## Contents
 1. [Overview](#overview)  
 2. [Control Processing functions](#2-control-processing-functions)  
    2.1 [PID ISA](#21-pid-isa)    
    2.2 [PID with anti-windup](#22-pid-with-anti-windup)    
 3. [Setpoint (SP) processing](#3-setpoint-processing) 
 4. [Process value(PV) processing](#4-process-value-processing)
 5. [Manual value (MV) processing](#5-manual-value-processing)
 6. [Control value (CV) processing](#6-control-value-processing )
 7. [Setpoint curve ceneration](#7-setpoint-curve-generation ) 
 8. [Signal processing](#8-signal-processing )
 9. [Benchmark](#9-benchmark )
 10. [Project summary](#10-project-summary)


## Overview
 
 library provide functionalities:
 
**P-I-D processing**
  - P, P-I ,P-D, P-I-D selection 
  - antiwind-up on/off selection 
  - control output rate limit (with alarm flag)
  - control error dead band on/off selection 
  - bias signal input 
   <!--  - I action auto-reset (with preloading) on/off selection -->
   
**Setpoint (SP processing) signal processing**
   
  - external/internal setpoint input selection
  - rate limit on/off selection  
  - signal limit function
  - normalization function
  - setpoit signal generation   
  
**Process Value (PV processing) signal processing**
  - signal linear normalization 
  - signal noise filtration
  - SQRT normalization on/off selection 

**Signal processing functions**
  - relay functions: simple relay, relay with hysteresis,  three-Step relay with Hysteresis
  - value limit, rate limit, 
  - deadband function
  - noise filter function
  - linear normalization , sqrt normalization
  - ( signal curve generation ) 
  
###### [Contents](./README.md#contents)

*py Files:
 ```python
├── [src]
│   ├── pid_isa.py                 see  p. 2.1 PID-ISA  
│   ├── pid_aw.py                  see  p. 2.2 PID with anti-windup  
│   ├── sp_processing.py           see  p.3  Setpoint Processing 
│   ├── pv_processing.py           see  p.4  Process Value Processing
│   ├── mv_processing.py           see: p.5. Manual value processing 
│   ├── curve_generator.py         
│   ├── utils_pid_esp32.py         see: (functional_description.md)
│     
├── [process_model]
│   ├── process_models.py
│   └── ....
│ 
├── [examples]
│   ├── anti_windup.py        
│   ├── sp_processing.py
├── [unit_tests]
└── ...
 
 ``` 


# 2. Control Processing functions

ALL PID alghoritms are implemented as uctypes.struct() for parameters storage and dedicated functions for processing.

## 2.1 PID-ISA 

<p align="center"> <img src="https://github.com/2dof/esp_control/blob/main/drawnings/pid_isa_schema_neg.png" width="500" height="300" />
<br> figure A1.</p>

discrete implementation of Two-Degree-of-Freedom PID Controller (standard form) described by:

$$ u=K_{p}[(br-y)+\frac{1}{T_{i}s}(r-y)+\frac{T_{d}s}{T_{m}s+1}(cr-y))]+u_{bias}$$ 
```math
\small   r: \text{setpoint; }\\
\small   y: \text{proces value; }\\
\small   b,c: \text{weighting parametes}
```
called by function: 
```python
def isa_updateControl(pid,sp,pv,utr = 0.,ubias = 0.):    # pid- pid-isa structure, sp -setpoint, pv -proces value, utr -tracking input, ubias -bias input;
```
which return control value.


**Setting up P-I-D controller**

 *pid* object is created as uctypes.struct() based on layout defined in  *ISA_REGS* dictionary. 
 *ISA_REGS* define all parametar and Configuration Register (defined by ISA_FIELDS dict (bit fields)):

```python
  form pid_isa import *
  
  pid_buf=bytearray(128)     # memory allocation 
  PID = uctypes.struct(uctypes.addressof(pid_buf), ISA_REGS, uctypes.LITTLE_ENDIAN)   # 
 
  isa_init0(PID)       # custom method for setting pid parameters
  isa_tune(PID)        #  recalculate parameters
```
All PID tunable parameters need to be initialized and Configuration setting selected by custom function ```isa_init0(PID) ```(or by direct acces) and recalculated by  ```isa_tune(PID) ``` function.

 ```isa_init0() ``` is a custom function for setting up parameters,but parameters are accesible directly from PID struct

 ```python
  PID.Kp = 2 
  PID.Ti = 1
  ...
  PID.Ts =0.1   # [sec]
  ...
  # P-i-D action selection
  PID.CFG.Psel = True
  PID.CFG.Isel = True
  PID.CFG.Dsel = True     # or set by direct bute value writing. 
  # PID.CFG_REG =0x07     # == Psel,Isel,Dsel = True
  
  isa_tune(PID)        # recalculate parameters
``` 
Configuration setting is selected by setting CFG register by setting bits ( ```PID.CFG.Psel = True ```) or by direct byte value writing ( ```pid.CFG_REG =0x07 ```).

:exclamation: → ALLWAYS CALL  ```isa_tune() ``` function after changing parameters

When setting, is finished then just call ```python isa_updateControl(pid,sp,pv,utr,ubias)  ```   in timer callback or in the loop every Ts interval.

Sometimes a reset of PID controller is nedded, then call ```isa_reset(PID)``` to reset the values of Pk, Ik, Dk , u, u1, ed1  ( = 0.0 ).  
   


**PID struct field description** 

P-I-D structure defined is by ISA_REGS dictionary (see in file pid_isa.py) , all parameters are defined as FLOAT32 type values.   

```python
PID.   
    Kp      -   proportional gain   
    Ti      -   integrator time   
    Td      -   derivative time 
    Tm      -   derivative filter time    
    Tt      -   antiwindup time     
    b       -   setpoint weight on proportional term    
    c       -   setpoint weight on derivative term     
    Umax    -   max limit of control   
    Umin    -   low limit of control   
    dUlim   -   control rate limit  
    Ts      -   sampling time         
    Deadb   -   error deadband value    
    Pk      -   calculated P-action value  
    Ik      -   calculated I-action value      
    Dk      -   calculated D-action value        
    Ki      -   calculated integrator gain        
    Kd      -   calculated derivative gain  
    ai      -   calculated parameter for I-action   
    bi      -   calculated parameter for I-action  
    ad      -   calculated parameter for D-action  
    bd      -   calculated parameter for D-action   
    ek      -   ek=(sp-pv)   control error    
    ed      -   ek=(c*sp-pv) control error for D-action   
    ep      -   ek=(b*sp-pv) control error for P-action    
    du      -   control rate value  du/dt     (calculated)   
    u       -   control value  (calculated)   
    ed1     -   store ed(k-1)   (calculated)
    u1      -   store u(k-1)    (caluclated) 
    CFG_REG -   Congfiguration register ( byte access)
    CFG     -   configurration register ( bit filelds access)   
```
  
bit field names:
```python
 CFG.
    Psel    - bit:0  - P-action selection 
    Isel    - bit:1  - I-action selection
    Dsel    - bit:2  - D-action selection
    Awsel   - bit:3  - Antiwindup selection
    Mansel  - bit:4  - Manual selection
    Modesel - bit:5  - Mode selection(0-direct, 1-indirect)
    Deadsel - bit:6  - Dead band selection
    Rlimsel - bit:7  - Rate limit selection    
```


###### [Contents](./README.md#contents) 


## 2.2 PID with anti-windup 

PID controllers with 'build in' Anti-windup.

  <table style="padding:4px">
  <tr>
     <td> <img src="https://github.com/2dof/esp_control/blob/main/drawnings/pid_aw_neg.png" width="400" height="225" /> 
     <br><p align="center">  figure A.3 </center><br> 
   
   ```python
  def pid_aw_updateControl(pid,sp,pv,ubias = 0.)
  ```
 </p></td>
     <td> <img src="https://github.com/2dof/esp_control/blob/main/drawnings/pid_awm_neg.png" width="400" height="225" />  
      <br><p align="center"> figure A.4 </center><br> 
      
  ```python
  def pid_awm_updateControl(pid,sp,pv,ubias = 0.,mv = 0.)
  ```
 </p></td>
  </tr> </table> 
  
Discrete implementations of PID Controller described by general equation:

$$ u = K_{p}[e_{k}+\frac{1}{T_{i}s}e_{k}+\frac{T_{d}s}{T_{m}s+1}e_{k})]+u_{bias}$$ 

$$ e_{k} = r - y $$ 

```math
\small   r: \text{setpoint SP; }\\
\small   y: \text{proces value PV; }\\
\small   u_{bias}: \text{ bias input}
```
with build-in Anti-windup (with back-calculation) scheme.

**Difference from P-I-D ISA**
- build in antiwindup. 
- backward difference approximation was used for I and D action ( PID-ISA: I-action: backward, D-action: Trapez approximation).
- no dead-band, no rate limit, no du/dt calculation, no SP and D-action weighting. 
- structure parameters are not compatible ( can't be used interchangeably). 




PID processing functions: 
 ```python
pid_aw.py 
    ├── PID_REGS = {...}                                        - dictionary description of pid structure      
    ├── def pid_aw_updateControl(pid,sp,pv ,ubias=0.)           - p-i-d controller with Anti-windup (back-calculation)
    ├── def pid_awm_updateControl(pid,sp,pv ,ubias=0, mv=0.)    - p-i-d controller with Anti-windup (back-calculation) and Auto/Man bumpless switching 
    ├── def pid_tune(pid)                                       - tune pid parameters   
    └── def pid_init0(pid)                                      - init pid parameters (function can be edited by user) 
 ``` 


# 3. Setpoint processing 

Setpoint Value processing called by function: 
```python
 def sp_update(spr,spi,spe = 0.0)    # spr- setpoint structure , spi - internal setpoint,spi - extermal setpoint
```
perform basic setpoint signal processig : linear normalization (for external setpoint), min/max and rate value limitation according
to selected configuration.
Internal setpoint is value set by user/signal generation, external setpoint is selected for example in cascade control configuration.

**Setting-up SP processing**

 *SPR* object is created as uctypes.struct() (size of 64 bytes) based on layout defined in  *SP_REGS* dictionary. 
 *SP_REGS# define all parametar and Configuration Register (defined by SP_FIELDS dict (bit fields)).
 
```python 
sp_buf=bytearray(64)   #  memory allocation
SPR = uctypes.struct(uctypes.addressof(sp_buf), SP_REGS, uctypes.LITTLE_ENDIAN)
sp_init0(SPR)

# tuning by direct acces
SPR.SpeaL = -100.
sp_tune(SPR)
``` 
All SPR tunable parameters need to be initialized and Configuration setting selected by custom function ```sp_init0(PID) ```(or by direct acces) and recalculated by  ```sp_tune(PID) ``` function.
 ```sp_init0(SPR) ``` is a custom function (edidet by user) for setting up parameters, also parameters are accesible directly from structure.

 When reset of SP structure is requred, then ```sp_reset(pid)``` function should be used.

:exclamation: → ALLWAYS CALL  ```sp_tune() ``` function after changing tunable parameters

SP structure fields description:
```python
SPR.
    SpLL    - SP low limit
    SpHL    - SP High limit
    SpeaL   - external SP norm aL point (x) 
    SpeaH   - external SP norm aH point (x) 
    SpebL   - external SP norm bL point (y) 
    SpebH   - external SP norm bH point (y) 
    Rlim    - rate limit value in unit/sec 
    Ts      - sampling time
    sp      - sp value
    sclin   - calucated scaling factor for linear normalizacion
    sp1     - previous sp value: sp(k-1) 
    dx      - calculated dx/dt value 
    CFG_REG - Congfiguration register ( byte access)
    CFG     - configurration register ( bit filelds access)  
 ```   
 bit field names:
 ```python   
 CFG.
    SPesel  - external setpoint selection (SPesel =True)  
    Rlimsel - SP rate limit selection (Rlimsel =True)   
    SPgen   - Setpoint Curve generation (SPgen = True)     
    f3      - for user definition   
    f4      -  ... 
    f5      -  ...
    F6      -  ...
    F7      -   for user definition  
 ```
 
 
 ###### [Contents](./README.md#contents)
 
# 4. Process value processing

Process Value processing called by function: 
```python
 def pv_update(pvr,pve,pvi = 0.0):    # pvr- pv structure , pve - external setpoint, pvi - internal setpoint value
```
perform basic process value signal processig: linear normalization, noise filter and sqrt normalization depending on the selected option.
 
two imput signals: external pv value (pve) is a physical sensor value measuring with ADC; internal process value (pvi) is selected for example in cascade control configuration.
     
**Setting PV processing**

 *PVR* object is created as uctypes.struct() (size of 74 bytes) based on layout defined in  *PV_REGS* dictionary. 
 *PV_REGS* define all parametar and Configuration Register (defined by PV_FIELDS dict (bit fields)):
 
 ```python
pv_buf=bytearray(72)   
PVR = uctypes.struct(uctypes.addressof(pv_buf), PV_REGS, uctypes.LITTLE_ENDIAN)
pv_init0(PVR)

# tuning by direct acces
PVR.PvaL = -100  
PVR.PvaH = 100.
PVR.PvbL = 0.0  
PVR.PvbH = 100.
pv_tune(PVR)
 ```

All proces value tunable parameters need to be initialized, and Configuration setting selected by custom function ```pv_init0(PID) ```(or by direct acces) and recalculated by  ```pv_tune(PID) ``` function.
 ```pv_init0(SPR) ``` is a custom function (edidet by user) for setting up parameters, also parameters are accesible directly from structure.

 When reset of SP structure is requred, then ```pv_reset(pid)``` function should be used.
 
:exclamation: → ALLWAYS CALL  ```pv_tune() ``` function after changing tunable parameters.
     
  ```python 
  PVR.
    PvLL     - Pv low limit   
    PvHL     - Pv High imit        
    PvaL     - Pv linear norm aL point (x)   
    PvaH     - Pv linear norm aH point (x)
    PvbL     - Pv linear norm bL point (y)
    PvbH     - Pv linear norm bH point (y)
    SqrtbL   - Pv sqrt   norm  bL point (y)
    SqrtbH   - Pv sqrt   norm  bL point (y)
    Ts       - Sampling time 
    Tf       - noise filter  time constans  
    pv       - process value
    yf       - filter value out
    sclin    -  calucated scaling factor for linear normalizacion 
    scsqrt   -   calucated scaling factor for sqrtnormalizacion
    CFG_REG  - Congfiguration register ( byte access)
    CFG      - configurration register ( bit filelds access)
  ```
 bit field names:
 ```python   
 CFG.
    Pvisel  - internal PV selection   
    Sqrtsel - SQRT normalization selection   
    Fltsel  - noise filter selection     
    f3      -  ...   
    f4      -  ... 
    f5      -  ...
    F6      -  ...
    F7      -   for user definition  
 ```
 
 ###### [Contents](./README.md#contents)
 
 
# 5. Manual value processing 

Manual Value (MV) processing called by function: 
```python
 def mv_update(mvr,dmv,tr =0.0)    # mvr- mv structure , dmv - change in manual value input  ,tr - tracking input
```
which perform basic manual value signal processig: incremental change from input dmv of manual value with tracking input (from control signal), limit
min/max value. 
#racking (of control value) ensure to bumples change during Auto/Manual control in control process  

**Setting-up MV processing**

 *MVR* object is created as uctypes.struct() (size of 41 bytes) based on layout defined in  *MV_REGS* dictionary. 
 *MV_REGS* define all parametar.
 
 ```python
 from mv_processing import *
 
 # setting up
 mv_buf=bytearray(41)   
 MVR = uctypes.struct(uctypes.addressof(mv_buf), MV_REGS, uctypes.LITTLE_ENDIAN)

 mv_init0(MVR)              # init 

 MVR.MvLL = 0.0             # lets set new saturation parameter MvLL  
 mv_tune(MVR)               # Alway tube parameter after changing 
 
 for i in range(0,40):      # do some testing  
        
    ytr = 2*sin(6.28*0.05*i)
 
    y = mv_update(MVR,dx,ytr)
    print("ytr:",ytr,"mv:",y)
    
    if i == 22: # check how increasing Tt affect mv output to track   
       #dx = 1. 
       MVR.Tt   =0.5  
       mv_tune(MVR)
 ``` 
 
All manual value tunable parameters need to be initialized, custom function ```MV_init0(MVR) ```(or by direct acces) and recalculated by  ```MV_tune(MVR) ``` function.
 ```MV_init0(SPR) ``` is a custom function (edidet by user) for setting up parameters, also parameters are accesible directly from structure.
 When reset of MV structure is requred, then use ```mv_reset(MVR)``` .
 
:exclamation: → ALLWAYS CALL  ```MV_tune() ``` function after changing tunable parameters.

From the code above we will get (waveforms ploted in thonny): 
 <p align="center"> <img src="https://github.com/2dof/esp_control/blob/main/drawnings/mv_tracking_signal_neg.png" width="500" height="150" />
<br> figure C1.</p>

Because we change ```MVR.MvLL = 0.0 ``` then manual value will be cut  off at bottom, aslo by changing value of Tf we affect the delay/lag of MV value. 

**Changing Tt or Tm**
   
  Tracking dynamic - increasing value of Tt (in relation to sampling time (Ts))introduce more lag effect (see figure C1.), for fast responce keep Tf<=0.1 Ts, 
  Incremental change of input dmv - both Tm and Tr acts as scaling factor ( ~ Tt/Tm)  for input dmv affecting output value.  
   
         
MV structure parameters:
 ```python
 MVR.
    MvLL   - Manual value Low Limit   ( set as 0.95-1.0 of control Umax)    
    MvHL   - Manual value High limit  ( set as 0. to 0.05 of control Umin)    
    Tt     - time constant for tracking input ( set to <=0.1 of Ts to fast responce)     
    Tm     - time constant for increment change of manual input      
    Ts     - sampling time        
    mvi    - Manual value before saturation checkong 
    mvo    - Manual value oputput 
    at     -  calculated, tracking block parameter 
    bt     -  calculated, tracking block parameter 
    ct     -  calculated, tracking block parameter 
 ```
 
MV processing functions: 
 ```python
mv_processing.py 
    ├── MV_REGS = {...}                 - dictionary description of mv structure      
    ├── def mv_update(mvr,dmv,tr =0.0)  - return manual value according to change in 'dmv' or 'tr' inputs, update internal states  
    ├── def mv_tune(mvr)                - recalulate internal parameters of mvr when tunable parameters are change. 
    ├── def mv_reset(mvr)               - reset internal state , manual value mv = 0 
    └── def mv_init0(mvr)               - edited by user, initialize  'mvr' structure.  
 ``` 
     
 ###### [Contents](./README.md#contents)
 
 # 6. Control value processing 


     ( in preparation)
     
     
 ###### [Contents](./README.md#contents)
 
 # 7. Setpoint Curve Generation 
 
  <table style="padding:4px">
  <tr>
     <td> <img src="https://github.com/2dof/esp_control/blob/main/drawnings/curve_gen_neg.png" width="600" height="250" /> .
     <br><p align="center"> figure B1.</p></td>
     <td> <img src="https://github.com/2dof/esp_control/blob/main/drawnings/curve_gen2_neg.png" width="250" height="150" />  
      <br><p align="center"> figure B2 </center></p></td>
  </tr> </table>

 Generation of curve is based on defining list of points coordinates consisting of time slices and out values (on end of time slice) (figure B1.)
 
 sp_ramp =[p0, p1, p2, ....pN]  , whrere 
 p0 = [t0,val0]      - t0 = 0  - always 0 as start point, start from val0  
 p1 = [t1,Val1]      - in slice of time t1, change value from val0 to val1 
 p2 = [t2,Val2]      - in slice of time t2, change value from val2 to val2  
 ...
 pN = [tN,ValN]  
 

 Then, supplying our curve profile to ```class Ramp_generator() ``` and defining time unit ( Time slices (intervals) can be only in seconds ('s') or minites ['m'] )
 we create curve generator based on line interpolation between every 2 points.
 
 Example: 
 We want to generate setpoint curve profile: start from actual Setpoint value SP_val and generate values every dt = Ts = 1 sec
 - first define starting point p0=[0,0.0], we assume we dont know what actual SP_val is so we assume value 0.0 (curve profile can be loaded from memory or a file.)
 - in 4 min go to 20 (p1=[4,20]),  
 - hold value 20 for 4 min (p2=[4,20.]), next
 - raise value to 50 in 2 min (p3=[2,50.]), next
 - hold value 50 for 4 min (p4=[4,50.]), next
 - drop value to 25 in 4 min ([4,25.]), next 
 -  hold value 25 for 4 min (p2=[4,25.]) 
 
 As in the example below we define our Ramp profile, and create Setpoint generator ```SP_generator```.
 When we are ready, we start generator  ```SP_generator.start(SP_val) ``` from actual Setpoint value. It causes to write SP_val to the starting point 
 (p0 = [0, SP_val]), and set ```Fgen = True  ```. from this moment, we allow to generate values by calling ```SP_generator.get_value(Ts) ``` which return
 next values every dt =Ts period (see figure B2.)
 When generation is finished (i.e last point of curve was generated, then flag  is reseted. ```SP_generator.Fgen = False  ``` and ```.get_value(Ts)``` will return   last generated value in next call. 
 
  ```python 
  from curve_generator import *
  
         #  p0    p1     p2     p3     p4     p5     p6
 Ramp =  [[0,0],[4,20],[4,20],[2,50],[4,50],[4,25],[4,25]] 
 
 Ts = 1.0   #  sampling time 

 SP_generator =Ramp_generator(Ramp, unit='m')   # create generator 
 
 SP_val  = 10.0                                 # at the moment of start generation SP_val =10.0
 
 SP_generator.start(SP_val)                     # we start (allow) to generate values
 
 for i in range(0,1400):                        # simulate a "control loop"
        
    y =  SP_generator.get_value(Ts)         
    print(y)
       
    if  SP_generator.Fgen == False:             # just brake the loop when done 
       break  
    # utime.sleep(Ts)

  ```  
 
  ```python class Ramp_generator()  ``` allow to stop (halt), resume generation, add point(on the end of profile), or load new ramp. 
  Aslo in any time can get elapsed or remaining time during generation (see description below).
 
 ```python
curve_generator.py 
    │──class Ramp_generator(object)     - Ramp generator __init__(Ramp,unit='m') -> Ramp: list of points,  unit: 'm'-> minutes, 's'->seconds              
    │         ├── .start(val0)          - command start allowing to generate values every call of .get_value(dt), dt: time interval    
    │         ├── .stop()               - stop generating, even if .get_value(dt) is called, only last value is returned before .stop()
    │         ├── .resume()             - resume generating after stop
    │         ├── .get_value(dt)        - generate next value in dt interval.  
    │         ├── .add_point([tn,valn]) - add new point to the end of ramp.  
    │         ├── .load_ramp(Ramp,unit) - load new ramp to generator (only when generator not active (Fgen=False) .  
    │         ├── .elapsed_time()       - return  time from start of generation in (hh,mm,ss)  format
    │         └── .remaining_time()     - return  remaining tome to end of generation in (hh,mm,ss)  format
    │ 
    └── def sec_to_hhmmss(sec)          - calculate (hh,mm,ss) time format  from given seconds (sec)
 
 ``` 
 
 Go to [LINK TO_EXAMPLE]  to learn hot to use in practial example.   
 
 
 
 
      
   
 ###### [Contents](./README.md#contents)

 # 8. Signal processing


     ( in preparation)
     
  
   [functional_description](functional_description.md)
     
 ###### [Contents](./README.md#contents)

# 9. Benchmark 

Condition for time measurment:
- for pid, sp, pv, mv, etc. processing all selectable configuration were selected (i.e pid-isa: Psel, Isel, Dsel, Awsel, Modesel, Deadsel, Rlimsel =True ) 
- results are rounded-up with 0.1 ms accuracy.

MicroPython v1.19.1 on 2022-06-18. 
    |   --------------------------   freq: 160M Hz
    │── isa_updateControl()           -  
    ├── pid_aw_updateControl()        - 0.5 ms 
    ├── pid_awm_updateControl()       - 0.5 ms        
    ├── sp_update()                   - 0.3 ms 
    ├── pv_update()                   -
    ├── mv_update()                   -
    ├── Ramp_generator.get_value()    -    
    └──     
 ``` 

An @timed_function() was used to time measure (see [Identifying the slowest section of code](https://docs.micropython.org/en/latest/reference/speed_python.html))



 ###### [Contents](./README.md#contents)
 
# 10. Project Summary 

:exclamation:
actually only this overview is public, code will be published later. 

*DOCUMENTATION*
  - [x] Project architecture and algorithms description (doc) - not public 
  - [#] micropython usage documentation  
 
**IMPLEMENTATION** 
  
  - [x] Python implementation ( code based on classes), :exclamation: - not public 
  - [x] Micropython implementation (code based on structures)  :exclamation: → IN PROGRESS (actually not public)
  - [ ] C implementation (code based on structures)   :exclamation: → IN PROGRESS (actually not public)

*Tools*
  - [ ] serial protocol communication ( data exchange and controller configuration) 
  - [ ] desktop APP for configuration, simulation and testing 

**END NOTE:** with hope in the future i will add more functionalities like:
  - more P-I-D alghorithms implementations 
  - PID controller autotuning functions 
  - more advanced API: Cascade, fed-forward control implementation examples 



 
 
