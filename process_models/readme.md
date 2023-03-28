

## Simple process models 

Files
 ```python
simple_models_esp.py 
    ├── def.discrete_FOP()    - First Order Process discrete model                                          
    ├── class FOPDT_model()   - First Order Process with Delay Time discrete model       
    ├── class ring_buffer()   - ring buffer ( for creatinf delay line)  
    ├── class dc_model()      - disctere dc motor model                                       
    └──                                     
 ``` 


## First Order Proces with Delay Time

First Order Proces with Delay time ```FOPDT_model() ``` described by diff. equation: 

$$ \tau\dot{y}(t) = - y(t) + K_{p}u(t-t_{d})$$ 
```math
\small   Kp: \text{ process gain }\\
\small   \tau : \text{proces time constans; }\\
\small   t_{d}: \text{time delay}\\
```

## Simple DC motor 
Discrete DC motor (permament magnet) model: ```dc_motor() ``` described by diff. equation:

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

DC motor $$\phi\ , dot(\phi\), i $$ are storend in _x0, _x1, _x2. Calling  ```.update(V, Td, Ts) will return angular speed (_x2). by defauld Td = 0.0 Nm, Ts =0.01 sec. Rotor angle position is calculated in rane 0 -  2 PI radians. 

:exclamation:
- static friction model not implemented.
- note that by substituting catalog values of pmdc motor parameters, model will compute higher speed value than real one (but time constants should be similar).
- to add Friction Torque (Tf) ( given from motor catalog) to the model:  ```Td += Tf*sign(sinmodel._x1)```, since micropython have not sign() math function implemented then use  if else condiition. 
- sampling time (Ts) for dc motor model should be at lest 5 times smaller than min(Te,tm), Te: electrical time constant, Tm: mechanical time constant.     

example:
```python 

    model = dc_motor()        
                            # model._x0  -> angular rotor position[rad]    
                            # model._x1  -> angular speed  [ rad/s]
                            # model._x2  -> current [A]
                            
print('model step responce')
    for i in range(0,100):
        yk = model.update(1.0)       # .update(self, V,Td=0,Ts=0.01)
        print(i, yk)

```


