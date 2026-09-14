GEATbx: Examples of Objective Functions
 
 

 
 
 
 
 
 
 
 
 
 
 
 
 
 1.11 Michalewicz's function 12
 Contents1.13 Easom's function
 
 
 
 
 
 
 
 
 
## 1 Parametric Optimization
 

 
 
 
 
### 1.12 Branins's rcos function
 

 
 
 The Branin rcos function [Bra72]
 is a global optimization test function. The function has 3 global
 optima.
 
 function definition
 fBran(x1,x2)=a&#183;(x2-b&#183;x1^2+c&#183;x1-d)^2+e&#183;(1-f)&#183;cos(x1)+e;
 

 a=1, b=5.1/(4&#183;pi^2), c=5/pi, d=6, e=10, f=1/(8&#183;pi);
 

 -5<=x1<=10, 0<=x2<=15.
 global minimum
 f(x1,x2)=0.397887;
 (x1,x2)=(-pi,12.275), (pi,2.275), (9.42478,2.475).
 
 
 
 This function is implemented in objbran.
 
 
 
 

GEA Toolbox: Main page | Tutorial | Algorithms | M-function index | Example functions





   This document is part of the Genetic and Evolutionary Algorithm Toolbox for use with Matlab (GEATbx).


   The Genetic and Evolutionary Algorithm Toolbox is not public domain.


   Copyright &#169; Hartmut Pohlheim, All Rights Reserved,
      (pohlheim@systemtechnik.tu-ilmenau.de).
