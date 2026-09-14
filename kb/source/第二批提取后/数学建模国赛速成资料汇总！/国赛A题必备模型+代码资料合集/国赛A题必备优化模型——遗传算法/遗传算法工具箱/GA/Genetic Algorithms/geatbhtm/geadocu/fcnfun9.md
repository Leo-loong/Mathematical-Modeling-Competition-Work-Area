GEATbx: Examples of Objective Functions

 1.7 Griewangk's function 8

 Contents1.9 Ackley's Path function 10

## 1 Parametric Optimization

### 1.8 Sum of different power

 function 9

 The sum of different powers is a commonly used unimodal test function.

 function definition

 f9(x)=sum(abs(x(i))^(i+1)),

 i=1:n;

 -1<=x(i)<=1.

 global minimum

 f(x)=0; x(i)=0, i=1:n.

 This function is implemented in objfun9.

GEA Toolbox: Main page | Tutorial | Algorithms | M-function index | Example functions

   This document is part of the Genetic and Evolutionary Algorithm Toolbox for use with Matlab (GEATbx).

   The Genetic and Evolutionary Algorithm Toolbox is not public domain.

   Copyright &#169; Hartmut Pohlheim, All Rights Reserved,

      (pohlheim@systemtechnik.tu-ilmenau.de).
