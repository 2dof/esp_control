

# ESP32 MIKROPYTHON CONTROL LIB

P-I-D control library for esp32 Micropython 

:exclamation:
actually only this overview is public, code will be published later. ANY QUESTIONS ? ->  Send a message 

<img src="https://github.com/2dof/esp_control/blob/main/drawnings/PID_diagram_neg.png" width="700" height="300" />


## Contents
 1. [Overview](#overview)  
 2. [Control Processing functions](#2-control-processing-functions)  
  2.1 [PID ISA](#11-pid-isa)
 3. Setpoint (SP) processing 
 4. Process (PV) processing
 5. Manual value (MV) processing 
 6. [Project summary](#5-project-summary )


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

# 2. Control Processing functions

ALL PID alghoritms are implemented as uctypes.struct() by  parameters storage and dedicated function for processing.

## 1.1 PID-ISA 

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
which return control value .

**Setting up P-I-D controller**

 *pid* object is created as uctypes.struct() based on layout defined in  *ISA_REGS* dictionary. 
 *ISA_REGS* define all parametar and Configuration Register (defined by ISA_FIELDS dict (bit fields)):

```python
  form pid_devices import *
  
  pid_buf=bytearray(128)     # memory allocation 
  PID = uctypes.struct(uctypes.addressof(pid_buf), ISA_REGS, uctypes.LITTLE_ENDIAN)   # 
 
  isa_init0(PID)       # custom method for setting pid parameters
  isa_tune(PID)        #  recalculate parameters
```
All PID tunable parameters need to be initialized and Configuration setting selected by custom function ```isa_init0(PID) ```(or by direct acces) and recalculated by  ```isa_tune(PID) ``` function.

 ```isa_init0() ``` is a custom function for setting up parameters,but parameters are accesible directly from PID struct:
 ```python
  PID.Kp = 2 
  PID.Ti = 1
  ...
  PID.Ts =0.1   # [sec]
  ...
  # P-i-D action selection
  PID.CFG.Psel = True
  PID.CFG.Isel = True
  PID.CFG.Dsel = True     # or: 
  # pid.CFG_REG =0x07     # == Psel,Isel,Dsel = True
  
  isa_tune(PID)        # recalculate parameters
  
``` 

Configuration setting is selected by setting CFG register by setting bits ( ```PID.CFG.Psel = True ```) or by direct byte value writing ( ```pid.CFG_REG =0x07 ```).

:exclamation: → ALLWAYS CALL  ```isa_tune() ``` function after changing parameters

PID struct field description: 
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
    du      -   control rate value     
    u       -   control value     
    ed1     -   store ed(k-1)   
    u1      -   store u(k-1)     
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


:exclamation: Form more info abaut settings see [link to cheat sheet]

###### [Contents](./README.md#contents)

# 3. Setpoint (SP) processing 


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
 ```   
 CFG.
    SPesel  - external setpoint selection   
    Rlimsel - SP rate limit selection    
    f2      - for user definition    
    f3      -  ...   
    f4      -  ... 
    f5      -  ...
    F6      -  ...
    F7      -   for user definition  
 ```
 
 ###### [Contents](./README.md#contents)
 
# 4. Process (PV) processing

     
  ```python 
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
 
# 5. Manual value (MV) processing 


     ( in prepatation)


# 6. Project Summary 

:exclamation:
actually only this overview is public, code will be published later. 

*DOCUMENTATION*
  - [x] Project architecture and algorithms description (doc) - not public 
  - [ ] micropython usage documentation  
 
**IMPLEMENTATION** 
  
  - [x] Python implementation ( coded based on classes), :exclamation: - not public 
  - [x] Micropython implementation (code based on structures)  :exclamation: → IN PROGRESS (actually not public)
  - [ ] C implementation (code based on structures)   :exclamation: → IN PROGRESS (actually not public)

*Tools*
  - [ ] serial protocol communication ( data exchange and controller configuration) 
  - [ ] desktop APP for configuration, simulation and testing 

**END NOTE:** with hope in the future i will add more functionalities like:
  - more P-I-D alghorithms implementations 
  - PID controller autotuning functions
  - more advanced API: Cascade, fed-forward control implementation examples 



 
 
