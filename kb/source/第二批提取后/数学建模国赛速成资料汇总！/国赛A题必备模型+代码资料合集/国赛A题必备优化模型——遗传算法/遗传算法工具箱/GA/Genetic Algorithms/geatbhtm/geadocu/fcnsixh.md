GEATbx: Examples of Objective Functions

 1.14 Goldstein-Price's function

 Contents2.1 Double integrator

## 1 Parametric Optimization

### 1.15 Six-hump camel back

 function

 The 2-D Six-hump camel back function [DS78]

 is a global optimization test function. Within the bounded region

 are six local minima, two of them are global minima.

 function definition

 fSixh(x1,x2)=(4-2.1&#183;x1^2+x1^4/3)&#183;x1^2+x1&#183;x2+(-4+4&#183;x2^2)&#183;x2^2;

 -3<=x1<=3, -2<=x2<=2.

 global minimum

 f(x1,x2)=-1.0316;

 (x1,x2)=(-0.0898,0.7126), (0.0898,-0.7126).

 This function is implemented in objsixh.

GEA Toolbox: Main page | Tutorial | Algorithms | M-function index | Example functions

   This document is part of the Genetic and Evolutionary Algorithm Toolbox for use with Matlab (GEATbx).

   The Genetic and Evolutionary Algorithm Toolbox is not public domain.

   Copyright &#169; Hartmut Pohlheim, All Rights Reserved,

      (pohlheim@systemtechnik.tu-ilmenau.de).
