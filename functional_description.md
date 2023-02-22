## Functional desciption ## 

 <table style="padding:4px"> <tr>
     <td>    <img src="https://github.com/2dof/esp_control/blob/main/drawnings/relay_graph.png" width="75" height="75">  </td>
   <td>   
    
  ```python
 y = relay2(0,1,0.5) # will return: -1
 y = relay2(0.6,1,0.5) # will return: 1      
```
    
 </td>
      </tr>
 </table>
 
     
 <font size="2" face="Courier New" >
 <table style="padding:4px">
  <tr>
     <td> ---------- </td>
     <td style="width:50%"> ----- Description ------  </td>
     <td style="width:50%">  example </td>
  <tr>
     <td  > <img src="https://github.com/2dof/esp_control/blob/main/drawnings/relay_graph.png" width="75" height="75"> </td>
   <td >  <em> simple relay </em><br>  <sub> description: y(x)= h for x>=w, -h otherwise  </sub>
   </td>
      <td>
       
 ```python
 #  y = relay2(x,h,w)    
 y = relay2(0,  1,  0.5) # will return: -1
 y = relay2(0.6, 1, 0.5) # will return: 1  
```
       
   </td>
  </tr>
   
 <tr>
     <td > <img src="https://github.com/2dof/esp_control/blob/main/drawnings/relay2h_graph.png" width="75" height="75">       </td>
     <td>   <em> Relay with hysteresis </em> <br>  <sub> description  </sub>  </td>
      <td> 
       
 ```python
 #  class relay2h(wL=-1.0,wH=1.0)   
 relay_2h=relay2h()       # -> init:(wL=-1,wH=1)    and state out: -1.0  
 
 y1 =  relay_2h.relay(0.0)   #   y1 = -1
 y2 =  relay_2h.relay(1.0)   #   y2 =  1.  
 y3 =  relay_2h.relay(2.0)   #   y2 =  1.   
 y4 =  relay_2h.relay(0.0)   #   y3 =  1.       
 y5 =  relay_2h.relay(-1.0)  #   y3 = -1.        
 y6 =  relay_2h.relay(-2.0)  #   y3 = -1.
 y7 =  relay_2h.relay(0.0)   #   y3 = -1.
```
   </td>
  </tr> 
   <tr>
     <td> <img src="https://github.com/2dof/esp_control/blob/main/drawnings/relay3_graph.png" width="75" height="75">   </td>
    <td>   <em> 3 step relay </em> <br>  <sub> description  </sub>  </td>
    <td>
       
 ```python
 #   y = relay3(x,h,w)  
     y1 = relay3(0.,1,0.5)    # y1 = 0.
     y2 = relay3(0.5,1,0.5)   # y2 = 1.
     y3 = relay3(-0.5,1,0.5)  # y3 = -1.
     
```
   </td>
  </tr>
    <tr>
      <td> <img src="https://github.com/2dof/esp_control/blob/main/drawnings/relay3h_graph.png" width="75" height="75">  </td>
     <td>   <em>  3 step relay with hysteresis  </em> <br>  <sub> description  </sub> </td>
   <td>
       
 ```python
 #  class relay3h(wL=0.5,wH=1)     and init state out: -1.0 
    
  x   = [-2.,-1.1,-1,-0.6,-0.5,0,0.5,0.9,1,2,1,0.6,0.5,0.4,0,-0.5,-1,-1.1,-2]   
  yref = [-1,-1,-1,-1, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0,-1,-1]   
  yout = []  
  
  relay_3h =relay3h()  # (wL=0.5,wH=1)
  
  for i in range(0,len(x3h)):
     y = relay_3h.relay(x[i])
     yout.append(y)  
  
  print(yref)
  print(yout)  
```
   </td>    
  </tr>
     <tr>
      <td> <img src="https://github.com/2dof/esp_control/blob/main/drawnings/limit_graph.png" width="75" height="75">   </td>
     <td>   <em> limit (saturation) function </em> <br>  <sub> description  </sub>  </td>  
      
   <td>
       
 ```python
 #  y = limit(x,HL,HH) 
    y1 = limit(0.5.,-1,1)  # y1 = 0.5
    y2 = limit(2.,-1,1)    # y2 = 1.
    y3 = limit(-2.,-1,1)   # y3 = -1
```
   </td>
  </tr>
     <tr>
      <td> <img src="https://github.com/2dof/esp_control/blob/main/drawnings/deadband_graph.png" width="75" height="75">  </td>
     <td>   <em> deadband function </em> <br>  <sub> description  </sub>   </td>
   <td>
       
 ```python
 #  y = deadband(x,w)
    y1 = deadband(0,0.5)    #  y1 = 0.
    y2 = deadband(0.5,0.5)  #  y2 = 0.
    y3 = deadband(1.,0.5)   #  y3 = 0.5
    y4 = deadband(-1.,0.5)  #  y4 = -0.5  
```
   </td>
  </tr>
      <tr>
      <td> <img src="https://github.com/2dof/esp_control/blob/main/drawnings/rateLimit_block.png" width="75" height="75">  </td>
     <td>   <em> rate limit </em> <br>  <sub> description  </sub>    </td>
   <td>
       
 ```python
 #  class ratelimit(dH=1,Ts=1) , init: 1 [unit/sec]  , Ts = 1
 #  y =ratelimit.limit(x) 
    
 rate=ratelimit(); 
    
 y1 = rate.limit(4)  #    y1 = 1
 y2 = rate.limit(4)  #    y2 = 2
 y3 = rate.limit(4)  #    y3 = 3
 print(rate.dx)      #    dx = 1 -> actual rate    
 y4 = rate.limit(4)  #    y4 = 4  
 y4 = rate.limit(4)  #    y4 = 4  
 print(rate.dx)      #    dx = 0 -> actual rate 
       
```
   </td>
  </tr>
   <tr>
      <td> <img src="https://github.com/2dof/esp_control/blob/main/drawnings/norm_graph.png" width="75" height="75">  </td>
     <td>   <em> linear normalization </em> <br>  <sub> description  </sub>  </td>
 
   <td>
       
 ```python
 #  class lin_norm(aL=0,aH=1,bL=0,bH=100) -> input form <0..1> to <0..100>

 norm = lin_norm()
 y1 = norm.normalize(0.5)  # y1 = 50   
 y2 = norm.normalize(1.0)  # y2 = 100
 y3 = norm.normalize(1.5)  # y2 = 150
```
   </td>
  </tr>
   <tr>
      <td> <img src="https://github.com/2dof/esp_control/blob/main/drawnings/norm_sqrt_graph.png" width="75" height="75"> </td>
     <td>   <em> SQRT normalization   </em> <br>  <sub> description  </sub>    </td>
     <td>
       
 ```python
 #  class sqrt_norm(bL=0,bH=100)
  
```
   </td>
 </tr> 
      
      
  
</table>

        
 
