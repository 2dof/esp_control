
## First Order Proces with Delay Time

First Order Proces with Delay time ```FOPDT_model() ``` described by diff. equation: 

$$ \tau\dot{y}(t) = - y(t) + K_{p}u(t-t_{d})$$ 
```math
\small   Kp: \text{ process gain }\\
\small   \tau : \text{proces time constans; }\\
\small   t_{d}: \text{time delay}
```

## Simple DC motor 
Discrete DC motor model: ```DC_motor_model() ``` described by diff. equation:

$$ L\dot{i} = V  -Ri+ K_{b}\dot{\phi}$$ 

$$ J\ddot{\phi} = K_{t}i -b_{b}\dot{\phi} - T_{d} $$ 

```math
\small   i: \text{ current [A] }\\
\small   \phi\: \text{ angle position [rad]}\\
\small   R: \text{ motor resistance [Ohm] }\\
\small   L : \text{motor inductance [H]}\\
\small   J : \text{rotor inertia [kg.m**2/s**2]}\\
\small   K_{t}: \text{torque constant (N-m/a)}\\
\small   K_{b}: \text{back emf constant (volt-sec/rad)}\\
\small   b_{m}: \text{motor mechanical damping [Nms]}\\
\small   T_{d}: \text{load torque [Nm]}\\
```


 ```python
simple_models_esp.py 
    ├── def.discrete_FOP()    - First Order Process discrete model                                          
    ├── class FOPDT_model()   - First Order Process with Delay Time discrete model       
    ├── class ring_buffer()   - ring buffer ( for creatinf delay line)  
    ├── class dc_model()      - disctere dc motor model                                       
    └──                                     
 ``` 
