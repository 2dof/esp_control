# MicroPython p-i-d-isa library
#The MIT License (MIT), Copyright (c) 2022-2023 L.Szydlowski
# __version__   = "1.0.0"
##https://github.com/2dof/esp_control

# just copied from https://github.com/2dof/esp_control/blob/main/src/utils_pid_esp32.py
# doc: relay with hysteresis  https://github.com/2dof/esp_control/blob/main/functional_description.md
class relay2h: 
    def __init__(self, wL=-1.0,wH=1.0):
        self.wL=wL
        self.wH=wH
        self._y_1= -1   
        
    def relay(self,x: float):
 
        if ((x>=self.wH)|((x>self.wL)&(self._y_1==1))):
            self._y_1=1.0      
            return 1 
        elif((x<=self.wL)|((x<self.wH)&(self._y_1==-1))):    
            self._y_1=-1.0
            return -1.0
 

class OnOff_controller(object):
    def __init__(self,hystL =-1 , hystH =1):
        
        if hystH> hystL : 
            self.relay =relay2h(hystL ,hystH)
        else:
            self.relay =relay2h(-1 ,1)  
        
        self.uk=0       
        self.ek = 0.0   
        
        self.Fstart = False  # 
        
    def start(self):         # start/stop calculationg control 
        self.Fstart = True
        
    def stop(self): 
        self.Fstart = False
        self.uk=0
        
    def tune(self,hystL,hystH):
        
        if hystH> hystL: 
            self.relay.wL = hystL
            self.relay.wH = hystH
        
        else: 
            self.relay.wL=-1      
            self.relay.wH= 1
            print('wrong Hysteresis params, must be: histL> histH')
            
    def reset(self): 
        
        self.relay.y_1=-1
        self.ek = 0.0
        self.uk =0
        
    def updateControl(self,sp,pv):
        
        self.ek = sp - pv 
        
        if self.Fstart:
        
            self.uk = self.relay.relay(self.ek)  # will return -1 or 1  so
            self.uk =(self.uk+1)//2              # we shift  to 0 to 1   
            
        else:
            self.reset() 
            
        return self.uk
    
    

if __name__ == '__main__':
     
    from simple_models_esp import FOPDT_model 
    from random import uniform 
        
    # simulation time init 
    Tstop=100
    Ts =  1          
    Ns=int(Tstop/Ts)

    #[1] process model FOPDT
    process_model = FOPDT_model(Kp=100.0,taup=100.0,delay=5.0, y0=21,Ts=Ts)

    #[2] On-Off Controller initialization
    hystL= -1
    hystH = 1    # width of hysteresis: hystH -  hystL
    controller = OnOf_controller(hystL ,hystH) 
    controller.start()
    
    #[3] simulation 
    sp = 50.     # setpoint
    yk  = 0.      # proces outpout value  
    uk  = 0.      # control value out
    
    for i in range(Ns):
        #[a] Read process value (in real time wee read from ADC and do pv processing)
        yk = process_model.update(uk)
        
        #vn = uniform(-0.5,0.5)  # white noise , we model some measurment noise   
        pv = yk #+ vn
        
       sp=50 #   
       if k*Ts >=250:
           sp = 40
           
        uk = controller.updateControl(sp, pv)
        
        print("sp:",sp,"pv:",pv,"uk:",uk)