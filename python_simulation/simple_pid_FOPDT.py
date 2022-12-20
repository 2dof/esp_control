# -*- coding: utf-8 -*-
"""
Created on Mon Dec 12 13:39:03 2022

@author: szydl
"""

import numpy as np
import matplotlib.pyplot as plt
plt.rcParams['lines.linewidth'] = 1
plt.rcParams['lines.markersize'] = 1
plt.rcParams["savefig.facecolor"]='white'
plt.rcParams["figure.facecolor"]='white'
plt.rcParams["axes.facecolor"]='white'
plt.ion() 
plt.close('all') 

from scipy.integrate import odeint

# specify number of steps
Tstop=50
Ts =0.1 
ns=int(Tstop/Ts)
# define time points
t = np.linspace(0,Tstop,ns+1)

# process parameters ----------------------------
Kp = 2.0            # static Gain
taup = 5.0          # time constans
thetap = 3.0        # proces delay 

 
# model of process without delay 

def process(y,t,u,Kp,taup):
    # Kp   : process gain
    # taup : process time constant
    dydt = -y/taup + Kp/taup * u
    return dydt

def process_step_response(t):
    # step responce of FOPDT (First-Order-process with Delay Time )
    # !! peroces delay is implemented as delay in input signal 
    # Input:
    # t : time points 
    # specify number of steps
    ns = len(t)-1
    delta_t = t[1]-t[0]  # sampling time 

    # storage for recording values
    uout = np.zeros(ns+1)  # controller output
    pv = np.zeros(ns+1)  # process variable

    # step input
    uout[1:]=2.0
     
    # Simulate time delay
    ndelay = int(np.ceil(thetap / delta_t))

    # loop through time steps    
    for i in range(1,ns):
        # implement time delay
        iop = max(0,i-ndelay)
        y = odeint(process,pv[i],[0,delta_t],args=(  uout[iop],Kp,taup))
        pv[i+1] = y[-1]
    return pv, uout


def simple_pid(sp,pv,sp_last,pv_last,I,dt):
    # ------------------
    # sp : setpoint
    # pv : proces value 
    # pv_last : last proces value
    # I = integral action
    # dt : sampling time, 
    # outputs ------
    # u : control value
    # P : proportional Action
    # I : integral action
    # D : derivative action
    
    # PID parameters 
    # Kp   = 0.1 # K
    # Ti = 5.0 # sec
    # Td = 2.0  # sec
    #---------------------------------------------------
    #Tuning based on IMC (internal Model Control) for 2-dof pid (see D action calculation comment:(!))  
    tauc = max(1*taup, 8*thetap)      #  'moderate' tutning
    #tauc = max(1*taup, 1*thetap)  #  'agressive' tuning 
    Kp   = ((taup+0.5*thetap)/(tauc+0.5*thetap))
    Ti   = (taup+0.5*thetap)
    Td   = taup*thetap/(2*taup+thetap)
    
    # --------------------------------------------------------
    # Tuning based on step Response Method (https://yilinmo.github.io/EE3011/Lec9.html)
    # read from figure(1) , step responce of system  ( see comment for D action calculation for standard pid controller )
 
   
    # Ko = 4/2   #  K0=(y-yo)/(u-uo): the system gain -> calculated from proces step responce
    # To = 5.0   # 
    # Lo = 3.    # 
    #  # calculate The PID parameters from Ziegler-Nichols Rules
    # Kp = 1.2*To/(Ko*Lo)
    # Ti = 2*Lo
    # Td = 0.5*Lo
    
    # --------------------------------------
    
    # PID Ki and Kd
    Ki = Kp/Ti 
    Kd = Kp*Td
    #upper and lower bounds on control output in %  
    outMin = 0.0   # 
    outMax = 100   # as % of max PWM clock 65535.0
    
    # calculate controll error 
    error = sp - pv

    # P action calculation
    P = Kp * error
    
    # I action 
    ie = Ki * error * dt  
    I = I + ie
  
    # D action : 
    D = Kd * ((pv - pv_last ) /dt)                  #(!)   for sp = const  we have 2-dof controller
    # D = Kd * ((error -( sp_last- pv_last)) /dt)    # (!!) standard pid controller   
    
    # calculate  control outout
    uout = P+I+D
    
    # Control saturation checking and anti-windup implementation 
    if (uout < outMin):
        uout = outMin
        I = I - ie     #  anti-reset windup 
        
    elif (uout > outMax):     
        uout = outMax
        I = I - ie    #  anti-reset windup 
                
    return[uout,P,I,D]



def pid_step_response(t):
    # t = time points 
 
    # specify number of steps
    ns = len(t) 
    delta_t = t[1]-t[0]  # sampling time 

    # storage for recording values
    sp = np.zeros(ns)  # setpoint
    uo = np.zeros(ns)  #  
    Po = np.zeros(ns)  #
    Io = np.zeros(ns)  #
    Do = np.zeros(ns)  #
    # step input
    sp[1:]=2.0
    pv      = 0.0
    pv_last = pv
    
    # PID precondition/initialization
    I = 0.0     # 
    uo[0] = 0.0 
    
    # loop through time steps    
    for i in range(1,ns):
        
        [uout,P,I,D] =simple_pid(sp[i],pv,sp[i-1],pv_last,I,delta_t)
        uo[i] = uout 
        Po[i],Io[i],Do[i] = P,I,D
        
    return uo, sp,Po,Io,Do

# calculate step response
 
pv,uo = process_step_response(t)   # process step responce

uo1,sp,Po,Io,Do = pid_step_response(t)

 
plt.figure(1)
plt.plot(t,pv,'b-',label=r'$y(t)$')
plt.plot(t,uo,'r-',label=r'$u(t)$')
plt.legend(loc='best'); plt.grid('True')
plt.ylabel('Process Output') ; plt.xlabel('t [s]')
plt.title('step responce off process')

plt.figure(2)
plt.subplot(2,1,1)
plt.plot(t,sp,'b-',label=r'$x(t)$')
plt.plot(t,uo1,'r-',label=r'$u(t)$') ;   
plt.legend(loc='best'); plt.grid('True')
plt.ylabel('  ')
plt.subplot(2,1,2)
plt.plot(t,Po,'r--',label=r'$P(t)$')
plt.plot(t,Io,'g--',label=r'$I(t)$')
plt.plot(t,Do,'b--',label=r'$D(t)$')
plt.legend(loc='best'); plt.grid('True')
plt.xlabel('t [s]')
 
# ========== PROCES CONTROL SIMULATION =================

#def process_step_response(t):
if  True:
    
    # step responce of FOPDT (First-Order-process with Delay Time )
    # !! peroces delay is implemented as delay in input signal 
    # Input:
    # t : time points 
    # specify number of steps
    ns = len(t)
    delta_t = t[1]-t[0]  # sampling time 
    


    # storage for recording values
    uo = np.zeros(ns)  # controller output
    pv = np.zeros(ns)  # process variable
    Po = np.zeros(ns)  #
    Io = np.zeros(ns)  #
    Do = np.zeros(ns)  #
    
    
    # Simulate time delay
    ndelay = int(np.ceil(thetap / delta_t))
    
    # --- setpoint generation 
    sp = np.zeros(ns)  # setpoint
    
    sp[20:]=50.0   # [C]
    

    # PID precondition/initialization
    I = 0.0        # reset Integral action 
    uout =  0.0    # initial control value     
    uo[0] = uout    
  
    #Proces value preconditions
    pv[0] = 0.0   # [Celsjus]     
    
    # process noise (use if neded) 
    mean = 0    
    std = 1
               

    # loop through time steps    
    for i in range(1,ns):
        
        #   FOPTD  simulation
        # implement time delay in control singal 
        iop = max(0,i-ndelay)
        u= uo[iop]             # delayed control 
        # process simulation  
        y = odeint(process,pv[i-1],[0,delta_t],args=(u,Kp,taup))
        # noise 
        nv = 0.0# 0.2 *np.random.normal(mean, std) # 
        
        pv[i] = y[-1] +nv     # measurment with white nosie, 
        
        pv_value  = pv[i]   
        #-----------------------------------------------
        
       # PID outout calculation 
        
        [uout,P,I,D] =simple_pid(sp[i],pv[i],sp[i-1],pv[i-1],I,delta_t)
        
        uo[i]=uout 
        Po[i],Io[i],Do[i] = P,I,D
        
        
        
    plt.figure(3)
    plt.plot(t,sp,'g-',label=r'sp(t)$')
    plt.plot(t,pv,'b-',label=r'$pv(t)$')
    plt.plot(t,uo,'r-',label=r'$u(t)$')
    plt.legend(loc='best'); plt.grid('True')
    plt.ylabel('Process Output') ; plt.xlabel('t [s]')
    plt.title('proces control simulatio') 
 

