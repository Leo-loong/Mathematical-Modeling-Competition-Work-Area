GEATbx: Examples of Objective Functions

 1.13 Easom's function

 Contents1.15 Six-hump camel back function

## 1 Parametric Optimization

### 1.14 Goldstein-Price's

 function

 The Goldstein-Price function [GP71]

 is a global optimization test function.

 function definition

 fGold(x1,x2)=[1+(x1+x2+1)^2&#183;(19-14&#183;x1+3&#183;x1^2-14&#183;x2+6&#183;x1&#183;x2+3&#183;x2^2)]&#183;[30+(2&#183;x1-3&#183;x2)^2&#183;(18-32&#183;x1+12&#183;x1^2+48&#183;x2-36&#183;x1&#183;x2+27&#183;x2^2)];

 -2<=x(i)<=2, i=1:2.

 global minimum

 f(x1,x2)=3;

 (x1,x2)=(0,-1).

 This function is implemented in objgold.

GEA Toolbox: Main page | Tutorial | Algorithms | M-function index | Example functions

   This document is part of the Genetic and Evolutionary Algorithm Toolbox for use with Matlab (GEATbx).

   The Genetic and Evolutionary Algorithm Toolbox is not public domain.

   Copyright &#169; Hartmut Pohlheim, All Rights Reserved,

      (pohlheim@systemtechnik.tu-ilmenau.de).
