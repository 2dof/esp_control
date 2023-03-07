

First Order Proces with Delay time ```FOPDT_model() ``` described by diff. equation: 

$$ \tau\dot{y}(t) = - y(t) + K_{p}u(t-t_{d})$$ 
```math
\small   Kp: \text{ process gain }\\
\small   \tau : \text{proces time constans; }\\
\small   t_{d}: \text{time delay}
```




 ```python
simple_models_esp.py 
    ├── def.discrete_FOP()    - First Order Process discrete model                                          
    ├── class FOPDT_model()   - First Order Process with Delay Time discrete model       
    ├── class ring_buffer()   - ring buffer ( for creatinf delay line)  
    ├──                                        
    └──                                     
 ``` 
