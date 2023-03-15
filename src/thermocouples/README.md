

Thermocouple lib implementa a ITS-90 thermocoule Temperature reference functions based on ITS-90 Polynomials from IEC 60584-1/2013.


source of polynomials: IEC 60584-1/2013 or https://www.omega.co.uk/temperature/z/pdf/z198-201.pdf)

Source of tables: [https://srdata.nist.gov/its90/main/0](https://srdata.nist.gov/its90/main/)

**Note**
Polynomials on nist site are for [mV] values but there are not valid since implementation based on them do not give results
like in tables. All polynomials in function implmentation are from IEC 60584, and they return results (in uV) consistent with NIST Tables.
Lookup tables are implemented NIST Tables.

from practical use 

Thermocouple Type K
          ├──model_K.py          # thermocoule type K model based on ITS-90 polynomials
          ├──its90_K.py          # caluclation Temperature (Celsius) based on ITS-90 Polynomials from IEC 60584-1/2013    
          ├──its90_K_lookup.py   # lookup table based on array.  Caluclation temperature from -270 C to 1370 C 
          ├──its90_K_blookup.py  # lookup table on  bytes. Caluclation temperature from 0.0 C to 1370 C       
          ├──lookup_search.py    #  
          
          
          
