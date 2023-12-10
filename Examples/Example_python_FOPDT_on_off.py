# -*- coding: utf-8 -*-
"""
Python Onoff R&D simulator for display 
data 

@author: 2dof
controller clasee/functions:
    relay2h()
    OnOf_controller)
    
process model classes/functions: 
    ring_buffer() 
    discrete_process()
    FOPDT_model()
"""


# model process  
class ring_buffer(object):
    def __init__(self, bufferSize =5):
        
        self.bufferSize = bufferSize 
        self.data     = np.zeros(bufferSize)
        self.ii  = 0    # index of next "head" position
        self.it  = 0    # index of tail position 
        self.ndata = 0  # No of data
            
    def add_data(self,data): 
        
          if self.ndata>=self.bufferSize:
              self.ndata-=1
        
          self.data[self.ii] = data
          self.ndata+=1
          self.ii = (self.ii+1) % self.bufferSize # 
   
    def get_data(self):
        
        if self.ndata ==0 :
            return []
            
        x = self.data[self.it] 
        self.ndata-=1
        self.it = (self.it+1) % self.bufferSize   # 

        return x
    
    
def discrete_process(y_1,Ts,u,Kp,taup):
   
    yk=  taup/(taup+Ts)*y_1 + Kp*Ts/(taup+Ts) * u
    return yk

class FOPDT_model(object):
    def __init__(self,Kp=2.0,taup=10.0,delay=3.0, y0=0.0,Ts=0.1):
        
        self.Kp    = Kp
        self.taup  = taup
        self.delay = delay
        self.Ts    = Ts
        self.y_1   = y0
        self.ndelay = int(self.delay/self.Ts)
        self.buf    = ring_buffer(bufferSize =self.ndelay+1)
        self.buf.ii = self.ndelay
        
    def update(self,u):
        
        self.buf.add_data(u)    # delay line
        uk=self.buf.get_data()
        yk= discrete_process(self.y_1,self.Ts,uk,self.Kp,self.taup)
        self.y_1 =yk 
        
        return yk 
    
#===Controller================================ =======
class relay2h(object):
    """relay 2 position with hysteresis  
        wL : low level of hysteresis
        wH : High level of hysteresis
    """
    def __init__(self, wL=-1,wH=1):
        self.wL=wL
        self.wH=wH
        self.y_1=-1    
        
    def get(self,x):
        """
        """        
        if ((x>=self.wH)|((x>self.wL)&(self.y_1==1))):
            self.y_1=1      
            return 1 
        elif((x<=self.wL)|((x<self.wH)&(self.y_1==-1))):    
            self.y_1=-1
            return -1


class OnOf_controller(object):
    def __init__(self,histL =-1 , histH =1):
        
        if histH> histL : 
            self.relay =relay2h(histL ,histH)
        else:
            self.relay =relay2h(-1 ,1)  
    
        self.uk=0       
        self.ek = 0.0   # sp-pv
        self.Fstart = False  # 
        
    def start(self):         # start/stop calculationg control 
        self.Fstart = True
        
    def stop(self): 
        self.Fstart = False
        self.uk=0
        
    def tune(self,histL,histH):
        
        if histH> histL: 
            self.relay.wL = histL
            self.relay.wH = histH 
        
        else: 
            self.relay.wL=-1      
            self.relay.wH= 1
            print('wrong Hysteresis params, must be: histL> histH')
            
    def reset(self):  # reset all internal state 
        
        self.relay.y_1=-1
        self.ek = 0.0
        self.uk =0
        
    def updateControl(self,sp,pv):
        
        self.ek = sp - pv
        
        if self.Fstart:
        
            self.uk = self.relay.get(self.ek)    # will return -1 or 1  so
            self.uk =(self.uk+1)//2          # we shift from 0 to 1  
            
        else:
            self.reset() 
            
        return self.uk


if __name__ == "__main__":
    
    from matplotlib.pylab import *
    import matplotlib.pyplot as plt
    plt.rcParams['lines.linewidth'] = 1.0
    plt.rcParams['lines.markersize'] = 2
    plt.rcParams["savefig.facecolor"]='white'
    plt.rcParams["figure.facecolor"]='white'
    plt.rcParams["axes.facecolor"]='white'
    plt.ion()
    matplotlib.pyplot.close
    
    from numpy import random
    
    # specify simulation time and number of steps 
    Tstop=1500           # total time simulation
    Ts =  0.25           # sampling time 
    Ns=int(Tstop/Ts)+1
    t = np.linspace(0,Tstop,Ns)  # define time vector (for plotting)
 
   #[1] process model FOPDT 
    yo=21     #  initial value (21 Celsjus)
    Lo=1      #  proces delay
    To=200    # process time constant 
    model = FOPDT_model(Kp=12.0,taup=To,delay=Lo, y0=yo,Ts=Ts)
       
    # just for plotting
    xsp = np.zeros(Ns)
    y   = np.zeros(Ns) 
    xu  = np.zeros(Ns)
    y0 = np.zeros(Ns)
    xe  = np.zeros(Ns)
    xupid  = np.zeros(Ns)
 
    # init simulation 
    sp = 50.     # setpoint
    yk  = 0.      # proces outpout value (measured)
    uk  = 0.      # control value 
    
    # ON-OFF controller initializasion 
    controller = OnOf_controller(-1,1)
    controller.start()
    
    # main simulation loop
    # yk           : proces output 
    # pv = yk +vk  : proces value measurement with measurement noise 
    # sp           : setpoint             
    # uk           : control output   
    # controller.ek: ek = sp-pv controll error
    
    for k in range(0,Ns):
       
       # proces simulation 
       yk=model.update(uk)
     
       # pv measuring (add measurement noise)
       vk =  random.uniform(0, 1) # 
       pv = yk +vk                  
       
 
       # change SP during simulation 
          
       if k*Ts >=250 and k*Ts<400:
            sp = 40
       
       if (k*Ts >=400) and (k*Ts <775):  
            sp+=0.04
           
       if (k*Ts >=1000) and (sp>40):  
            sp-=0.04
           
       
         
           
       # update control 
       uk = controller.updateControl(sp, pv)
     
       # save data
       xsp[k], y[k], xu[k],xe[k]= sp,pv,uk ,controller.ek             
   
 
       uk = uk*1   # gain = 0 
       
       
    # plot sumulation results   
    plt.close('all')
    fig, (ax1, ax2) = plt.subplots(2, sharex=True)
    ax1.plot(t,xsp,'r-',label=r'$sp$')
    ax1.plot(t,y,'b-',label=r'$pv$') 
    ax1.set_xlabel('t[s]')
    ax1.grid(True); ax1.legend(fontsize=10)
         
    ax2.plot(t,xu,'r-',label=r'$uk$') 
    #ax2.plot(t,xe,'g-',label=r'$ek$') 
    ax2.set_xlabel('t[s]')
   #ax2.plot(t,xupid,'r--',label=r'$upidk$') 
    ax2.grid(True); ax2.legend(fontsize=10)
    
 
     
 
    