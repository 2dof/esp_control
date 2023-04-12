
from machine import Timer 
import utime
from machine import Pin, ADC
import esp32
import uasyncio as asyncio
from benchmark import timed_function


from pid_aw import *            # pid alghoruthm 
#from mv_processing import *     

def pid_init(pid):
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
    
# parameters can be load/safe from/to file     
    def load_from_file(pid_controller,file_name=''):  
        print(' load parameters from file')
        pass

    def save_to_file(pid_controller,file_name=''):  
        print('safe parameters to file')
        pass


#------------------------------------------------------------
class pid_awm_controller(object):
    def __init__(self,Kp,Ti,Td,Tm,Tt,Umax=100,Umin =0 ,dUlim=100,Ts = 1.0):
        
        self.pid_buf=bytearray(101)  # size of PID_REGS is 101 bytes, 
        self.pid = uctypes.struct(uctypes.addressof(self.pid_buf), PID_REGS, uctypes.LITTLE_ENDIAN)
        
        #-local params copy ( our "menu system" can store params, and later we can recalculate variables)  
        self.Kp = Kp      
        self.Ti = Ti        
        self.Td = Td        
        self.Tm = Tm       
        self.Tt = Tt           
        self.Umax = Umax     
        self.Umin = Umin       
        self.dUlim = dUlim    
        self.Ts    =  Ts  
    
        self.tune()     # do not forget perform recalculation self.pid structure
        
        self.Fparam=False  # no parameter to update
        # ----------
        # select P-I config
        self.pid.CFG.Psel = True
        self.pid.CFG.Isel = True
        self.pid.CFG.Dsel = False
        

        
   # @timed_function    
    def updatecontrol(self,sp,pv,ubias=0.,mv=0.):
        
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
        print(self.pid.Kp,self.pid.Ti) 
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


if __name__ == '__main__':

    from simple_models_esp import FOPDT_model
 
    # simulation time amd sampling
    Ts =.25
    Tstop= 500
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
        if i*Ts >=150:
           sp = 30

        if i*Ts >=300:
           sp = 60
           
        #[a] Read process value (in real time wee read from ADC and do pv processing)
        yk = process_model.update(uk)
        #vn = uniform(-0.4,0.4)  # white noise  
        pv = yk #+ vn
    
        uk = controller.updatecontrol(sp,pv)  # dafault ubias=0, mv = 0
        
        print("sp:",sp,"pv:",pv,"uk:",uk)
        #print("sp:",sp,"pv:",pv,"uk:",uk,'mv:',mv)
#--boot.y-----------------------
# derive
# SP_IN = ADC(Pin(36))
# SP_IN.atten(ADC.ATTN_11DB) #the full range voltage: 3.3V           
# SP_IN.width(ADC.WIDTH_10BIT)
# 
# pot_value = SP_IN.read()
# print('---')
# print(pot_value)

#----------------------------        



#--------------------------------------
#
# timer = Timer(0)
#  
# Control=pid_controller()
#  
# Control.timer = timer
# utime.sleep_ms(500)

      
 
# ##timer.init(period=Control.Ts, mode=Timer.PERIODIC, callback=Control.handleInterrupt)  
# 
 
   
 
# 
# 
# def handleInterrupt(timer):
#     global CNT, Ncalls, t0
#     
#     delta = utime.ticks_diff(utime.ticks_ms(), t0)
#     print(delta)
#     
#     tf = esp32.raw_temperature()
#     tc = (tf-32.0)/1.8
#     print("T = {0:4d} deg F or {1:5.1f}  deg C".format(tf,tc))
#     t0 = utime.ticks_ms()
#     
#     if CNT >= Ncalls:
#         timer.deinit()
#         print('timer stopped')
#     
#     CNT+=1
#     
# print('timer one shot')
# 
# timer = Timer(0)
# t0 = utime.ticks_ms() 
# timer.init(period=1000, mode=Timer.PERIODIC, callback=handleInterrupt)