GEATbx: Examples of Objective Functions
 
 

 
 
 
 
 
 
 
 
 
 
 
 
 
 1.6 Schwefel's function 7
 Contents1.8 Sum of different power function 9
 
 
 
 
 
 
 
 
 
## 1 Parametric Optimization
 

 
 
 
 
### 1.7 Griewangk's function 8
 

 
 
 Griewangk's function is similar to Rastrigin's function. It has
 many widespread local minima. However, the location of the minima
 are regularly distributed.
 
 function definition
 f8(x)=sum(x(i)^2/4000)-prod(cos(x(i)/sqrt(i)))+1,
 i=1:n;

 -600<=x(i)<= 600.
 
 
 
  
 
 global minimum
 f(x)=0; x(i)=0, i=1:n.
 
 
 
 This function is implemented in objfun8.
 
 
 
 
 
 
 
 
 
 
 

GEA Toolbox: Main page | Tutorial | Algorithms | M-function index | Example functions





   This document is part of the Genetic and Evolutionary Algorithm Toolbox for use with Matlab (GEATbx).


   The Genetic and Evolutionary Algorithm Toolbox is not public domain.


   Copyright &#169; Hartmut Pohlheim, All Rights Reserved,
      (pohlheim@systemtechnik.tu-ilmenau.de).
