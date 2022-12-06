
ESP32 MIKROPYTHON CONTROL LIB
=============================
<img src="https://github.com/2dof/esp_control/blob/main/drawnings/pid_block_schema_neg.png" width="600" height="240" />

:exclamation: 
See Poject sumary below :exclamation: 
 

Standard PID control library for esp32 Micropython, raspberryPi (python) and C implementation  
 

Basic architecture of control lib will be based on PID-ISA Control shematic  with
additional functionalities: 

Main functionalities of Controller
**PID**
  - P, PI ,PD, PID selection
  - antiwind-up on/off selection
  - control output rate limit (with alarm flag)
  - control error dead band on/off selection
  - I action auto-reset (with preloading) on/off selection 
  - bias signal input 
  
**Setpoint (SP processing) signal processing**
   
  - external/internal setpoint input selection
  - rate limit on/off selection and alarm indication
  - signal limit function
  - normalization function
  - setpoing block generation
  
**Process Value (PV processing) signal processing**
  - signal normalization 
  - signal noise filtration
  - SQRT normalization on/off selection 

** Manual Value (MV Processing) signal processing**
  - Tracking Value from control value output (bumpless Manual/Auto switching)
  - signal limit 
  

:exclamation: 
At this stage all work has 'private' status, after ported project from Python version 
and perform test, project will be moved to 'public'
 

**Project Summary**

:exclamation:
actually only this overview is public, code wil be published after validation

===============
**DOCUMENTATION**
  - [x] Project architecture and algorithms description (doc) - not public 
  - [ ] micropython usage documentation  
 
**IMPLEMENTATION** 
  
  - [x] Python implementation ( coded based on classes), :exclamation: - not public 
  - [x] Micropython implementation (code based on structures)  :exclamation: → IN PROGRESS (actually not public 
  - [ ] C implementation (code based on structures)   :exclamation: → IN PROGRESS (actually not public)

**Tools**
  - [ ] serial protocol communication ( data exchange and controller configuration) 
  - [ ] desktop APP for configuration , simulation and testing 

**END NOTE:** with hope in the future i will add more functionalities like:
  - PID controller autotuning functions
  - more advanced API: Cascade, fed-forward control implementation examples 
 

  
 Functional desctiption 
 ====================== 
 
[Functional description](functional_description.md)


