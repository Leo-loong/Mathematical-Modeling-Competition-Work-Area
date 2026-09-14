GEATbx: Examples of Objective Functions

 1.8 Sum of different power function 9

 Contents1.10 Langermann's function 11

## 1 Parametric Optimization

### 1.9 Ackley's Path function

 10

 Ackley's Path [Ack87]

 is a widely used multimodal test function.

 function definition

 f10(x)=-a&#183;exp(-b&#183;sqrt(1/n&#183;sum(x(i)^2)))-exp(1/n&#183;sum(cos(c&#183;x(i))))+a+exp(1);

 a=20; b=0.2; c=2&#183;pi; i=1:n;

 -32.768<=x(i)<=32.768.

 global minimum

 f(x)=0; x(i)=0, i=1:n.

 This function is implemented in objfun10.

GEA Toolbox: Main page | Tutorial | Algorithms | M-function index | Example functions

   This document is part of the Genetic and Evolutionary Algorithm Toolbox for use with Matlab (GEATbx).

   The Genetic and Evolutionary Algorithm Toolbox is not public domain.

   Copyright &#169; Hartmut Pohlheim, All Rights Reserved,

      (pohlheim@systemtechnik.tu-ilmenau.de).
