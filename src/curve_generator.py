# MicroPython p-i-d-isa library
#The MIT License (MIT), Copyright (c) 2022-2023 L.Szydlowski
#https://github.com/2dof/esp_control

#from benchmark import timed_function
#import utime


#@timed_function
def sec_to_hhmmss(sec):
    hh = sec // 3600
    sec %= 3600
    mm = sec // 60
    sec %= 60
    
    return (hh, mm, sec)    
  

class Ramp_generator(object):
        def __init__(self,Ramp,unit='m'):

           self.Fgen: bool = False
           self.load_Ramp(Ramp,unit)    
               
        def add_point(self,pnt): 
    
            self.Ramp[-1]=pnt 
            self.Ramp.append(pnt)
            self._Npts  = len(self.Ramp)-1
            self._Nsec +=pnt[0]*self.unitval
            
        def load_Ramp(self,Ramp,unit='m'): 
            
            if not self.Fgen:
                
               self.unit  = unit
               self.unitval = 60 if (self.unit=='m') else 1
               self.Ramp = Ramp
               self.Ramp.append(Ramp[-1])
               self._Npts = len(self.Ramp) -1
               self._nk   = 0
               self._Cnt  = 0
               self._Tcnt = 0.          
               self.value = 0.
               self._Nsec = int(0) 
               
               for pnt in self.Ramp[0:-1]:
                   self._Nsec += pnt[0]
               
               self._Nsec *= self.unitval    
                           
               if len(self.Ramp)>1: 
                   self._Cnt=self.Ramp[1][0]*self.unitval
               
               return True    
            
            else:  
                return False
            
        def start(self,val0=0):
            
            if val0 != 0:
                 self.Ramp[0]=[0,val0]    
            
            self.Fgen=True
            self._Tcnt = 0
            
            if len(self.Ramp)>1: 
               self._Cnt=self.Ramp[1][0]*self.unitval
            else:
               self.Fgen=False
                  
        def resume(self):
            
            if (self._Tcnt <self._Nsec):
                self.Fgen=True 
               
        def stop(self):   
            self.Fgen=False
            
        #@timed_function     
        def get_value(self,Ts: float)-> float:    
            
            if self.Fgen:
                self.value = self.Ramp[self._nk+1][1] - (self._Cnt/(self.Ramp[self._nk+1][0]*self.unitval))*(self.Ramp[self._nk+1][1]-self.Ramp[self._nk][1])             
                
                self._Cnt-= Ts
                self._Tcnt+=Ts             
                
                if (self._Cnt<=0): 
                    self._nk+=1
          
                    if (self._nk > (self._Npts-1)): 
                       self._nk=self._Npts-1 
                       
                    self._Cnt=self.Ramp[self._nk+1][0]*self.unitval
                     
                if  (self._Tcnt >self._Nsec)&(self.value==self.Ramp[self._Npts][1]): 
                    self.Fgen=False
    
            return self.value
        
        def elapsed_time(self):
        
            return sec_to_hhmmss(self._Tcnt)
    
        def remaining_time(self):
            
            return sec_to_hhmmss(self._Nsec-self._Tcnt+1)
    

if __name__ == "__main__":
    
    Rampa =  [[0,0],[4,20],[4,20],[2,50],[4,50],[4,25],[4,25]]
    Rampb= [[0,0],[4,40],[4,40],[2,100],[4,100],[4,50],[4,50]]
    
    Ts=1
    
    SP_generator =Ramp_generator(Rampa, unit='s')
    
    SP_generator.add_point([5,10])
    
    # SP_generator.load_Ramp(Rampb,unit='s') # or 
   
    SP_generator.start(val0=10)

    for i in range(0,1400): 
        
        y = SP_generator.get_value(Ts)
        
        print(y)
        #print(SP_generator.elapsed_time())
        #print(SP_generator.remaining_time())
        #if i==20: SP_generator.stop()
        #utime.sleep(1)
        if SP_generator.Fgen ==False:
             
            break



 
 