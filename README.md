
ESP32 MIKROPYTHON CONTROL LIB
=============================

Standard PID control library for esp32 Micropython implementation  
 

Basic architecture of control lib will be based on PID-ISA schematic (see PID_ISA_SCHEMA.pdf) with
additionals functionalities as for control outout value postprocessing (not shown on schematic):
- relays: 2, 3 positional relays (with or without histeresis)
- dead band function for control error value
-- pulse generator for binary manipulated value output

Main functionalities
**PID**
  - P, PI ,PD, PID selection
  - antiwind-up on/off selection
  - control output rate limit (with alarm flag)
  - control error dead band on/off selection
  - I action autoreset (with preloading) on/off selection 
  - bias signal input
  
**Setpoint (SP) signal processing**
  - Tracking Value on/off selection (from external setpoint intput when selected)
  - external setpoint input selection
  - rate limt on/off selection and 
  - signal saturation 
  
**Proces Value (PV) signal processing**
  - signal normalization 
  - signal noise filtration
  - SQRT normalization on/off selection 

** Manula Value (MV) signal processing**
  - Tracking Value from control valule output (bumpless Manual/Auto switching)
  - signal saturation 
  

:exclamation: 
At this stage all work has 'private' status, after ported project from Python version 
and perform test, project will be moved to 'public'
 

Project Summary
===============
**DOCUMENTATION**
  - [x] Project architecture and algorithms description (doc) - not public 

**IMPLEMENTATION**
  - [x] Python inplementation ( Fast prototyping and tresting) - not public  
  - [ ] Micropython implementation   :exclamation: - IN PROGRESS
  
**Tools**
  - [ ] serial protocol comunication ( data excange and controller configuration) 
  - [ ] desctop APP for configuration , simulation and testing

**END NOTE:** with hope in the future i will add more functionalities like:
  - Setpoint curve generation functions
  - PID controller autotuning functions
  - more advanced API: Cascade , fedforward control implementation examples 
 

  
  
 
 
