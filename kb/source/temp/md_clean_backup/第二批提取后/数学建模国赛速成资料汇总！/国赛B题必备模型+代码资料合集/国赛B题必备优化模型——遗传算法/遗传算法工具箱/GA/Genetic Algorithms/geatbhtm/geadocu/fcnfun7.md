GEATbx: Examples of Objective Functions
 
 

 
 
 
 
 
 
 
 
 
 
 
 
 
 1.5 Rastrigin's function 6
 Contents1.7 Griewangk's function 8
 
 
 
 
 
 
 
 
 
## 1 Parametric Optimization
 

 
 
 
 
### 1.6 Schwefel's function 7
 

 
 
 Schwefel's function [Sch81]
 is deceptive in that the global minimum is geometrically distant,
 over the parameter space, from the next best local minima. Therefore,
 the search algorithms are potentially prone to convergence in
 the wrong direction.
 
 function definition
 f7(x)=sum(-x(i)&#183;sin(sqrt(abs(x(i))))),
 i=1:n;

 -500<=x(i)<=500.
 
 
 
  
 
 global minimum
 f(x)=-n&#183;418.9829; x(i)=420.9687,
 i=1:n.
 
 
 
 This function is implemented in objfun7.
 
 
 
 

GEA Toolbox: Main page | Tutorial | Algorithms | M-function index | Example functions





   This document is part of the Genetic and Evolutionary Algorithm Toolbox for use with Matlab (GEATbx).


   The Genetic and Evolutionary Algorithm Toolbox is not public domain.


   Copyright &#169; Hartmut Pohlheim, All Rights Reserved,
      (pohlheim@systemtechnik.tu-ilmenau.de).
