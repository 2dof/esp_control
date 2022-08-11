
ESP32 MIKROPYTHON CONTROL LIB
=============================

Standard PID control library for esp32 Micropython implementation  
 

Basic architecture of control lib will be based on PID-ISA schematic (see PID_ISA_SCHEMA.pdf) with
additional functionalities as for control output value post-processing (not shown on schematic):
- relays: 2, 3 positional relays (with or without hysteresis)
- dead band function for control error value
-- pulse generator for binary manipulated value output

Main functionalities
**PID**
  - P, PI ,PD, PID selection
  - antiwind-up on/off selection
  - control output rate limit (with alarm flag)
  - control error dead band on/off selection
  - I action auto-reset (with preloading) on/off selection 
  - bias signal input
  
**Setpoint (SP) signal processing**
  - Tracking Value on/off selection (from external setpoint input when selected)
  - external setpoint input selection
  - rate limit on/off selection and 
  - signal saturation 
  
**Process Value (PV) signal processing**
  - signal normalization 
  - signal noise filtration
  - SQRT normalization on/off selection 

** Manual Value (MV) signal processing**
  - Tracking Value from control value output (bumpless Manual/Auto switching)
  - signal saturation 
  

:exclamation: 
At this stage all work has 'private' status, after ported project from Python version 
and perform test, project will be moved to 'public'
 

Project Summary
===============
**DOCUMENTATION**
  - [x] Project architecture and algorithms description (doc) - not public 
  - [ ] micropython usage documentation 
 
**IMPLEMENTATION**
  - [x] Python implementation ( Fast prototyping and testing) - not public  
  - [ ] Micropython implementation   :exclamation: - IN PROGRESS
  
**Tools**
  - [ ] serial protocol communication ( data exchange and controller configuration) 
  - [ ] desktop APP for configuration , simulation and testing 

**END NOTE:** with hope in the future i will add more functionalities like:
  - Set-point curve generation functions
  - PID controller autotuning functions
  - more advanced API: Cascade , fed-forward control implementation examples 
 

  
 Functional desctiption 
 ====================== 
 
Relay
![alt text](https://github.com/2dof/esp_control/blob/main/drawnings/relay_graph.png " ")
  
 
 
