#MIT License
#Copyright (c) 2023 Lukasz Szydlowski,  
## simple_models_esp.py - discrere models of LTI process  
 
import array
from RingBuffer import ring_buffer

def discrete_FOP(y_1,Ts,u,Kp,taup):
    yk=  taup/(taup+Ts)*y_1 + Kp*Ts/(taup+Ts) * u
    return yk

#First Order Process with delay time
class FOPDT_model(object):
    def __init__(self,Kp=2.0,taup=5.0,delay=3.0, y0=0.0,Ts=0.1):
        
        self.Kp    = Kp
        self.taup  = taup
        self.delay = delay
        self.Ts    = Ts
        self.y_1   = y0
        self.ndelay = int(self.delay/self.Ts)
        self.buf    = ring_buffer(bufferSize =self.ndelay+1)
        self.buf.ii = self.ndelay
     
    def update(self,u):
        
        self.buf.add_data(u)    
        uk=self.buf.get_data() #
        yk= discrete_FOP(self.y_1,self.Ts,uk,self.Kp,self.taup)
        self.y_1 =yk 
        
        return yk 
 

# ---------------------------------------
class dc_motor():
    def __init__(self,Ts =0.01,R=2.0,L =0.5 ,Kt=0.1,Kb= 0.1,bm=0.2,J=0.02):
              
        self.R = R        
        self.L = L        
        self.Kt =Kt       
        self.Kb = Kb      
        self.bm = bm      
        self.J = J        
        self._x0 = 0.     # phi [rad]  
        self._x1 = 0.     # dot(phi) [rad/s]
        self._x2 = 0.     # i: current [A]
        
    def update(self, V,Td=0,Ts=0.01):
        
        self._x0 = self._x0 + Ts* self._x1 
        self._x1 = self._x1 + Ts/self.J*(self.Kt*self._x2 - self.bm*self._x1 - Td)
        self._x2 = self._x2 + Ts/self.L*(V - self.R*self._x2 - self.Kb*self._x1)
        self._x0 -= (self._x0//6.2832) * 6.2832
        return self._x1   


if __name__ == '__main__':
    
    model =  FOPDT_model()  #dc_motor() # 
    print('model step responce')
    for i in range(0,100):
        yk = model.update(1.0)
        print(i, yk)
        
   
    