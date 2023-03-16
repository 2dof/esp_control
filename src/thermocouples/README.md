

Thermocouple library implements a ITS-90 thermocouple Temperature reference functions based on ITS-90 Polynomials from IEC 60584-1/2013 and
NIST Thermoelectric Voltage Lookup Tables


source of polynomials: IEC 60584-1/2013 or https://www.omega.co.uk/temperature/z/pdf/z198-201.pdf)

Source of tables: [https://srdata.nist.gov/its90/main/0](https://srdata.nist.gov/its90/main/)


## Thermocouple type K 

**Note**
Polynomials on the NIST site are for [mV] values, but they are not valid since implementation based on them do not give results
like in tables. All polynomials in function implementation are from IEC 60584, and they return results (in uV) consistent with NIST Tables.
Lookup tables are implemented based on  NIST Tables. 

implemented Tables are based on full decimal values from NIST. 
Go to [Benchmark](benchmark) to select best function for your needs (seed and memory size).


Function: ```its90model_K(temp)``` return EMV value [μV] for input temp [C] 
```
from model_K import its90model_K 

T = 250      #[C]  

E = its90model_K(T)        # E is EMF, expressed in microvolts (μV);

```
 
Function: ``` its90_K(E) ``` calculate Temperature in [C] for input E expressed in microvolts (μV), implementation based on Polynomials
```python
from its90_K import its90_K

E = 10153          # [uV] ->  250 [C]

T= its90_K(E)
```

function:```its90_K_lookup(E,low=0, high=163) ``` calculate Temperature in [C] for input E expressed in microvolts (μV), implementation based on approximation form  lookup table in range of E for temp: -270 to 1370  .

```python
from its90_K_lookup import its90_K_lookup

E = 10153            # [uV] ->  250 [C]

T,idx = its90_K_lookup(E[i])
T,idx = its90_K_lookup(E[i],idx-1,idx+1)

```

function ``` its90_K_blookup(E,low=0, high=137) ``` calculate Temperature in [C] for input E expressed in microvolts (μV), implementation based bytes lookup table
in range of E for temp: 0 to 1370.

```python 
from its90_K_blookup import its90_K_blookup

E = 10153    # [uV] ->  250 [C]

T,idx = its90_K_blookup(E)
T,idx = its90_K_blookup(E,idx-1,idx+1) 
```





```

Thermocouple Type K
          ├──model_K.py          # thermocoule type K model based on ITS-90 polynomials
          ├──its90_K.py          # caluclation Temperature (Celsius) based on ITS-90 Polynomials from IEC 60584-1/2013    
          ├──its90_K_lookup.py   # lookup table based on array.  Caluclation temperature from -270 C to 1370 C 
          ├──its90_K_blookup.py  # lookup table on  bytes. Caluclation temperature from 0.0 C to 1370 C       
          ├──lookup_search.py    #  
          
```          
 
          
## Benchmark 

```
ESP32: MicroPython v1.19.1  
freq : 160M Hz                                     tables
     |                         the worst           size  
     ├──model_K()                 x                  x
     ├──its90_K()             0.704 ms              672 bytes  - stored as 3 arrays of float32   
     ├──its90_K_lookup()      0.705 ms             1072 bytes  - stored as array of uint16 (165 values)
     ├──its90_K_blookup()     0.824 ms              276 bytes  - stored as bytes ( 138 values)
 ```
       
 details: [benchmark.txt](https://github.com/2dof/esp_control/blob/main/src/thermocouples/benchmark.txt)       
             
 Calculations speed based on lookups can be improved if we limit the scope of table search using
 returned index from previous calculation and use to limit search bonduary.
 
 ```python 
 lo = 0 
 hi = len(_ITS90_EKB)//2)-1
 
 T,idx = its90_K_blookup(E,lo,hi)
 
 lo , hi =idx-1 idx+1

 T,idx = its90_K_lookupB(E,lo,hi)
 ...  
 ```   
 With such an approach we able to speed casculations up x1.5/2, but it is nessesary to implement 
 condition for recalculation on full range when value will be out of actual bonduaries.
 
 ## AD849x series amplifiers 
 
 On [AN-1087: Thermocouple Linearization..](https://www.analog.com/en/app-notes/an-1087.html) notes, the author describedhow to use the NIST Lookup Table to perform Linearity Correction for AD849x or when they are used outside of their measurement range (Table 1. AD849x ±2°C Accuracy Temperature Ranges). 
 
 **Note**
 Remember that AD849x correction functiona use measutment in mV and You need to convert to uV for using with provided
 function. 
 
 ```python
    Vout = 1.0* 1000    # [mV]   
    #Trj  = 25          #[mV] Reference junction Temp.
    Vref = 0.0          #[mV] 
    Gain = 122.4
    #Cjc  = 4.95        #(mV/°C)
    Voffset = 1.25      # [mV]
     
    
    #[2]AD849x NIST Thermocouple Nonlinearity Compensation
    Euv = (Vout - Vref -Voffset)/Gain *1000    #*1000  mV  
    
    Tmj = its90_K_blookup(Euv)                #  using Lookup table
    Tmj2 = its90_K(Euv)                       #  using polynomials func. 
 
 ```
 
 
  ## AD7793 and ADT7320 
 
In [measuring-temp-using-thermocouples](https://www.analog.com/en/analog-dialogue/articles/measuring-temp-using-thermocouples.html), authorsdescribed measurement method (section: Measurement Solution 2: Optimized for Accuracy and Flexibility) based on AD7793 as the main ADC instrumentation amplifierfor thermocouple junction voltage measurement; an ADT7320 for reference junction temperature compensation; and a mirocontroller as the main calculation unit.

By implementing thermocouple functions or lookup tables in the microcontroller, we can build a universal measurement unit for all types of thermocouples.









 
