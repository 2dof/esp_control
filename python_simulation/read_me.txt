Python simple simulation but can be adapted to micropython

simple_pid_FOPDT.py : simple pid control for first order proces with delay time. script simulate:
                      - proces step responce 
                      - pid controller step responce 
                      - proces control simulation 
                      
  functions: 
  process(y,t,u,Kp,taup): firs order proces G=K/(Ts+1) ( without delay
  
  process_step_response(t)): step responce with FOPDT , where delay time   has been taken into input signal (step signal)
                        G(s)=P(s)/U(s) =>K/(Ts+1) * exp(-tau*s) => 
                        P= K/(Ts+1) exp(-tau*s) * U(s) -> K/(Ts+1) u(t-tau) 
                         
  
  pid_step_response(t): calculate pid step responce
  
  
  simple_pid(sp,pv,sp_last,pv_last,I,dt) : implemnt simple pid alghoritms with pid parameters tutning rules for 
                                            two pid alghoritm: standard pid and 2-dof pid ( differ from calculation
                                            of D action (standard pid: D=Kd * de/dt (e=sp=pv) , 
                                            2dof pid: D=Kd dpv/dt  (pv - process value)
                                            
                                            
                                           
                           
                          
    
