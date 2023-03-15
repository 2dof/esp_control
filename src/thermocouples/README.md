

Thermocouple library implements a ITS-90 thermocoule Temperature reference functions based on ITS-90 Polynomials from IEC 60584-1/2013.


source of polynomials: IEC 60584-1/2013 or https://www.omega.co.uk/temperature/z/pdf/z198-201.pdf)

Source of tables: [https://srdata.nist.gov/its90/main/0](https://srdata.nist.gov/its90/main/)

**Thermocouple type K**

**Note**
Polynomials on nist site are for [mV] values but there are not valid since implementation based on them do not give results
like in tables. All polynomials in function implmentation are from IEC 60584, and they return results (in uV) consistent with NIST Tables.
Lookup tables are implemented NIST Tables. 

Examples:

function: ``` def its90model_K(temp) ```` return EMV value [μV] for input temp [C] 
```
from model_K import its90model_K 

T = 250      #[C]  

E = its90model_K(T)        # E is EMF, expressed in microvolts (μV);

```
 
function: ```def its90_K(E) ```  
```
from its90_K import its90_K

E = 10153          # [mV] ->  250 [C]

T= its90_K(E)
```



function:``` def its90_K_lookup(E,low=0, high=163) ```
```
from its90_K_lookup import its90_K_lookup

E = 10153            # [mV] ->  250 [C]

T,idx = its90_K_lookup(E[i])
T,idx = its90_K_lookup(E[i],idx-1,idx+1)

```



function ``` def its90_K_blookup(E,low=0, high=137) ```
```
from its90_K_blookup import its90_K_blookup

E = 10153    # [mV] ->  250 [C]

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
          
          
***Benchmark***

ESP32: MicroPython v1.19.1 on 2022-06-18.  
freq : 160M Hz                                     tables
     |                         the worst           size  
     ├──model_K()                 x                  x
     ├──its90_K()             0.704 ms              672 bytes  - stored as 3 arrays of float32   
     ├──its90_K_lookup()      0.705 ms             1072 bytes  - stored as array of uint16 (165 values)
     ├──its90_K_blookup()     0.824 ms              276 bytes  - stored as bytes ( 138 values)
 
       
 details: [benchmark.txt](https://github.com/2dof/esp_control/blob/main/src/thermocouples/benchmark.txt)       
             
 Calculations speed based on lookups can be improve if we limit the scope of table search if we will use 
 returned index from previous calculation and use to limit search bonduary:
 
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
 
