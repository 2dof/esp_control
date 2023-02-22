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
 
     
 
 <table style="padding:4px,font-size:12px">
  <tr>
     <td> ---------- </td>
     <td style="width:50%"> Description </td>
     <td style="width:50%">  example </td>
  <tr>
     <td  > <img src="https://github.com/2dof/esp_control/blob/main/drawnings/relay_graph.png" width="75" height="75"> </td>
      <td >  <em> simple relay </em><br>   description: y(x)= h for x>=w, -h otherwise  
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
     <td>   <em>   </em> description   </td>
      <td>
       
 ```python
 #  class relay2h(wL=-1.0,wH=1.0)   
  
```
   </td>
  
  </tr>
   <tr>
     <td> <img src="https://github.com/2dof/esp_control/blob/main/drawnings/relay3_graph.png" width="75" height="75">   </td>
    <td>   <em>   </em> description   </td>
    <td>
       
 ```python
 #   y = relay3(x,h,w)  
  
```
   </td>
  </tr>
    <tr>
      <td> <img src="https://github.com/2dof/esp_control/blob/main/drawnings/relay3h_graph.png" width="75" height="75">  </td>
     <td>   <em>    </em> description  </td>
   <td>
       
 ```python
 #  class relay3h(wL=0.5,wH=1)   
  
```
   </td>
     
  </tr>
     <tr>
      <td> <img src="https://github.com/2dof/esp_control/blob/main/drawnings/limit_graph.png" width="75" height="75">   </td>
     <td>   <em>  </em> limit description  </td>  
      
      
 
 
  </tr>
     <tr>
      <td> <img src="https://github.com/2dof/esp_control/blob/main/drawnings/deadband_graph.png" width="75" height="75">  </td>
     <td>   <em>  </em> deadband  description   </td>
  </tr>
  </tr>
     <tr>
      <td> <img src="https://github.com/2dof/esp_control/blob/main/drawnings/norm_graph.png" width="75" height="75">  </td>
     <td>   <em>  </em> norm  description   </td>
  </tr 
 
   </tr>
     <tr>
      <td> <img src="https://github.com/2dof/esp_control/blob/main/drawnings/norm_sqrt_graph.png" width="75" height="75"> </td>
     <td>   <em>   </em> norm  description   </td>
  </tr 
      
      
  
</table>

        
 
