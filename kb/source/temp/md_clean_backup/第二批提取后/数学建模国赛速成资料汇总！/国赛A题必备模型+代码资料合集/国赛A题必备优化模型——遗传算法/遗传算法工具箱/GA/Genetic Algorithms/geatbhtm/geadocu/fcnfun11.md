GEATbx: Examples of Objective Functions
 
 

 
 
 
 
 
 
 
 
 
 
 
 
 
 1.9 Ackley's Path function 10
 Contents1.11 Michalewicz's function 12
 
 
 
 
 
 
 
 
 
## 1 Parametric Optimization
 

 
 
 
 
### 1.10 Langermann's function
 11

 
 
 The Langermann function is a multimodal test function. The local
 minima are unevenly distributed.
 
 function definition
 f11(x)=-sum(c(i)&#183;(exp(-1/pi&#183;sum((x-A(i))^2))&#183;cos(pi&#183;sum((x-A(i))^2)))),
 i=1:m, m=5;

 0<=x(i)<=10.

 For the value of A and c look at the mfile
 objfun11.
 
 
 
  
 
 global minimum
 f(x)=-1.4 (for m=5); x(i)=???,
 i=1:n.
 
 
 
 This function is implemented in objfun11.
 
 
 
 

GEA Toolbox: Main page | Tutorial | Algorithms | M-function index | Example functions





   This document is part of the Genetic and Evolutionary Algorithm Toolbox for use with Matlab (GEATbx).


   The Genetic and Evolutionary Algorithm Toolbox is not public domain.


   Copyright &#169; Hartmut Pohlheim, All Rights Reserved,
      (pohlheim@systemtechnik.tu-ilmenau.de).
