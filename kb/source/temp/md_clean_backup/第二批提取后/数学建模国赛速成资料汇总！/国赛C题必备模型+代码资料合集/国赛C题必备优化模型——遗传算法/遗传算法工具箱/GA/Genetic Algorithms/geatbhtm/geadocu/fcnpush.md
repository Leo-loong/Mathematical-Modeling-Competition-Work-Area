GEATbx: Examples of Objective Functions
 
 

 
 
 
 
 
 
 
 
 
 
 
 
 2.3 Harvest system
 Contents
 
 
 
 
 
 
 
 
## 2 Optimization of dynamic
 systems

 
 
 
 
### 2.4 Push-cart system

 
 
 The push-cart system [Mic92]
 is a two-dimensional system described by the following equations:
 

 x1(k+1)=x2(k),
 k=1,2,...,N,

 x2(k+1)=2&#183;x2(k)-x1(k)+(1/N^2)&#183;u(k).
 The objective function for minimization is therefore defined
 as:
 

 f(x,u)=-x1(N+1)+1/(2&#183;N)&#183;sum(u(k)^2),
 k=1:N.
 
 
 
  
 
 The exact solution can be analytically found by:
 

 Minimum=-(1/3)+((3&#183;N-1)/(6&#183;N^2))+1/(2&#183;N^3)&#183;sum(k^2),
 k=1:N-1.
 
 
 
  
 
 Figure 1 shows the control vector
 for the push-cart system with N=20.
 
 Fig. 1: Optimal control vector
 for the push-cart system with N=20
 
 
 
 This function is implemented in the m-file objpush.m.
 
 

GEA Toolbox: Main page | Tutorial | Algorithms | M-function index | Example functions





   This document is part of the Genetic and Evolutionary Algorithm Toolbox for use with Matlab (GEATbx).


   The Genetic and Evolutionary Algorithm Toolbox is not public domain.


   Copyright &#169; Hartmut Pohlheim, All Rights Reserved,
      (pohlheim@systemtechnik.tu-ilmenau.de).
