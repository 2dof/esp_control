

Thermocouple lib implementa a ITS-90 thermocoule Temperature reference functions based on ITS-90 Polynomials from IEC 60584-1/2013.


source of polynomials: IEC 60584-1/2013 or https://www.omega.co.uk/temperature/z/pdf/z198-201.pdf)

Source of tables: [https://srdata.nist.gov/its90/main/0](https://srdata.nist.gov/its90/main/)

**Note**
Polynomials on nist site are for [mV] values but there are not valid since implementation based on them do not give results
like in tables. All polynomials in function implmentation are from IEC 60584, and they return results (in uV) consistent with NIST Tables.
Lookup tables are implemented NIST Tables.

from practical use 

```
Thermocouple Type K
          ├──model_K.py          # thermocoule type K model based on ITS-90 polynomials
          ├──its90_K.py          # caluclation Temperature (Celsius) based on ITS-90 Polynomials from IEC 60584-1/2013    
          ├──its90_K_lookup.py   # lookup table based on array.  Caluclation temperature from -270 C to 1370 C 
          ├──its90_K_blookup.py  # lookup table on  bytes. Caluclation temperature from 0.0 C to 1370 C       
          ├──lookup_search.py    #  
          
```          
          
          
Benchmark

```
 	         	   its90_K()		    its90_K_lookup()	   its90_K_lookup()	
no.	Tref	[ms]	calc value	 [ms]	calc value          [ms]	calc value
----     -------   --------------------            ------------------            --------------------
1	-270	0.704	-245.7565		0.705	-270.0	         1.131	(-162.7)
2	-110	0.398	-109.9817		0.411	-110.0	         0.804	(-97.028)
3	10	0.377	9.956843		0.415	10.00	         0.759	10.0
4	25	0.368	24.98365		0.330	24.987	         0.783	25.0
5	250	0.383	249.9873		0.386	250.02	         0.799	250.024
6	500	0.377	499.9819		0.416	500.00	         0.538	500.0
7	555	0.326	555.0363		0.415	555.01	         0.781	555.012
8	600	0.317	599.9939		0.357	600.00	         0.590	600.0
9	665	0.324	664.9790	    	0.385	665.00	         0.779	665.0
10	770	0.316	770.0056		0.418	770.02	         0.782	770.024
11	776	0.324	776.0187		0.410	776.03	         0.786	776.029
12	910	0.324	909.9952		0.416	909.99	         0.705	909.9999
13	1200	0.335	1200.021		0.408	1200.00	         0.533	1200.0
14	1373	0.323	1372.044		0.439	1372.01	         0.824	1372.006

```
             
             
