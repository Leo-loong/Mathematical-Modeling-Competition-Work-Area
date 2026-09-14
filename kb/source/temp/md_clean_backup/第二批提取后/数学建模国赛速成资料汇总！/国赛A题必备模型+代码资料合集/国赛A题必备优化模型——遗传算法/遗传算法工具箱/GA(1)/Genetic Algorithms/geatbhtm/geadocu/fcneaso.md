GEATbx: Examples of Objective Functions
 
 

 
 
 
 
 
 
 
 
 
 
 
 
 
 1.12 Branins's rcos function
 Contents1.14 Goldstein-Price's function
 
 
 
 
 
 
 
 
 
## 1 Parametric Optimization
 

 
 
 
 
### 1.13 Easom's function

 
 
 The Easom function [Eas90]
 is a unimodal test function, where the global minimum has a small
 area relative to the search space. The function was inverted for
 minimization.
 
 function definition
 fEaso(x1,x2)=-cos(x1)&#183;cos(x2)&#183;exp(-((x1-pi)^2+(x2-pi)^2));
 

 -100<=x(i)<=100, i=1:2.
 
 
 
  
 
 global minimum
 f(x1,x2)=-1;
 (x1,x2)=(pi,pi).
 
 
 
 This function is implemented in objeaso.
 
 
 
 
 
 
 
 
 
 

GEA Toolbox: Main page | Tutorial | Algorithms | M-function index | Example functions





   This document is part of the Genetic and Evolutionary Algorithm Toolbox for use with Matlab (GEATbx).


   The Genetic and Evolutionary Algorithm Toolbox is not public domain.


   Copyright &#169; Hartmut Pohlheim, All Rights Reserved,
      (pohlheim@systemtechnik.tu-ilmenau.de).
