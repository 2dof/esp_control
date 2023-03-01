# -*- coding: utf-8 -*-
# utils_pis_esp32_ MicroPython utils library for pid control library
##https://github.com/2dof/esp_control
#The MIT License (MIT), Copyright (c) 2022-2023 L.Szydlowski
#__version__   = "1.0.0"

from math import fabs, sqrt

def limit(x,HL,HH):  
    
      if (x>=HH):
          return HH
      elif (x<=HL):
          return HL
      else:
          return x
        
def deadband(x,w): 
    
     if (x>w):
          return x-w
     elif (x<-w):
          return x+w
     else:
          return 0
        
def relay2(x,h,w): 
   
    if (x>=w):
        return h 
    else:
        return -h
        
def relay3(x,h,w): 
    
     if (x>=w):
        return h
     elif (x<=-w):
        return -h
     else:
        return 0


class relay2h: 
    
    def __init__(self, wL=-1.0,wH=1.0):
        self.wL=wL
        self.wH=wH
        self._y_1=-1    
        
    def relay(self,x: float):
 
        if ((x>=self.wH)|((x>self.wL)&(self._y_1==1))):
            self._y_1=1.0      
            return 1 
        elif((x<=self.wL)|((x<self.wH)&(self._y_1==-1))):    
            self._y_1=-1.0
            return -1.0
 
class relay3h: 
 
    def __init__(self, wL=0.5,wH=1):
        self.wL=wL
        self.wH=wH
        self._y_1=0
    
    def relay(self,x):
        if ((x>=self.wH)|((x>self.wL)&(self._y_1==1))):
            self._y_1=1          
            return 1 
        elif((x>=-self.wL)&(x<=self.wL)|((x<self.wH)&(self._y_1==0)&(x>=-self.wH))):    
            self._y_1=0
            return 0
        if ((x<-self.wH)|((x<-self.wL)&(self._y_1==-1))):  
            self._y_1=-1          
            return -1 
        

class lin_norm: 
    def __init__(self, aL=0,aH=1,bL=0,bH=100):
        self.__aL   =   aL
        self.__aH   =   aH
        self.__bL   =   bL
        self.__bH   =   bH
        self.__scale_calc()
    
    def __scale_calc(self):
        self._scale =  (self.__bH-self.__bL)/(self.__aH-self.__aL) 
    
    @property
    def aL(self):
        return self.__aL
    
    @aL.setter
    def aL(self, value):            
        self.__aL = value
        self.__scale_calc() 
        
    @property
    def aH(self):
        return self.__aH
    
    @aH.setter
    def aH(self, value):            
        self.__aH = value
        self.__scale_calc()  
    @property
    def bL(self):
        return self.__bL
    
    @bL.setter
    def bL(self, value):            
        self.__bL = value
        self.__scale_calc()
   
    @property
    def bH(self):
        return self.__bH
        
    @bH.setter
    def bH(self, value):            
        self.__bH = value
        self.__scale_calc()
          
    def normalize(self,x):
              
        return (x-self.__aL)*self._scale+self.__bL
              
        
class sqrt_norm: 
    def __init__(self,bL=0,bH=100):
   
        self.__bL  =   bL
        self.__bH  =   bH
        self._scale =  (self.__bH-self.__bL)/10
        
        def __scale_calc(self):
            self._scale =  (self.__bH-self.__bL)/10
    
        @property
        def bL(self):
            return self.__bL
    
        @bL.setter
        def bL(self, value):            
            self.__bL = value
            self.__scale_calc()

        @property
        def bH(self):
            return self.__bH
    
        @bH.setter
        def bH(self, value):            
            self.__bH = value
            self.__scale_calc()
                
    def normalize(self,x):
        
        return self._scale*sqrt(x)+self.__bL
        
class ratelimit:        
        def __init__(self,dH=1,Ts=1):
            self.dH=dH
            self.Ts=Ts
            self.x_1=0
            self.fh =False
            self.dx = 0
            
        def reset(self,x0=0):
            self.x_1=x0  
         
        def limit(self,x):
        
            self.dx = x-self.x_1                
            delta=self.dH*self.Ts
                
            if (fabs(self.dx)<delta):
                self.x_1=x
                self.fh =False
                return x
            else:
                y=self.x_1+delta
                self.dx  = delta
                self.x_1 = y    
                self.fh  = True
                return y
            
# To do:   a1 = Tf/(Tf+Ts) , b1 =Ts/(Tf+Ts) to avoid recalucaling            
def lp_filter(x,y_1,Ts,Tf):
    
    y=  Tf/(Tf+Ts)*y_1 +Ts/(Tf+Ts) * x
    return y


     

    
 
    