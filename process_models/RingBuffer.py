import array
from benchmark import timed_function

# ring bufffer for float data
class ring_buffer(object):
    def __init__(self, bufferSize =5,dtype='f'):
        
        self.bufferSize = bufferSize 
        self.data     =  array.array(dtype, [0]*bufferSize)
        self.it  = 0    # index of tail position 
        self.ndata = 0  # No of data
        self.ii =0      # index of nex head
        
    @micropython.native
    def any(self):
        if self.ndata ==0:
            return False
        return True
    
 
    @micropython.native
    def add_data(self,value): 
        
          if self.ndata>=self.bufferSize:
              self.ndata-=1 # overflow
              self.it = (self.it+1) % self.bufferSize 
        
          self.data[self.ii] = value
          self.ndata+=1
          self.ii = (self.ii+1) % self.bufferSize
          
    @micropython.native
    def get_data(self):
        
        if self.ndata ==0 :
            return None
            
        x = self.data[self.it] 
        self.ndata-=1
        self.it = (self.it+1) % self.bufferSize   # 

        return x
    

#  
# buf    = ring_buffer(bufferSize =5)
#  
# buf.add_data(1)
# buf.add_data(2)
# buf.add_data(3)
# buf.add_data(4)
# buf.add_data(5)
# buf.add_data(6)
# print('--')
# buf.get_data()
# buf.get_data()