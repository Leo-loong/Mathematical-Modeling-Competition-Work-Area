GEATbx: Examples of Objective Functions

 2.2 Linear-quadratic system

 Contents2.4 Push-cart system

## 2 Optimization of dynamic

 systems

### 2.3 Harvest system

 The harvest system [Mic92]

 is a one-dimensional equation of growth with one constraint:

 x(k+1)=a&#183;x(k)-u(k), k=1,2,...,N;

 such that x(0)=x(N).

 The objective function for minimization is therefore defined

 as:

 f(u)=-sum(sqrt(u(k))), k=1:N.

 The exact solution can be analytically found by:

 Minimum=-sqrt((x(0)&#183;(a^N-1)^2/(a^(N-1)&#183;(a-1))).

 Figure 1 shows the control vector

 for the harvest system with N=20.

 Fig. 1: Optimal control vector

 for the harvest system with N=20

 This function is implemented in objharv.

GEA Toolbox: Main page | Tutorial | Algorithms | M-function index | Example functions

   This document is part of the Genetic and Evolutionary Algorithm Toolbox for use with Matlab (GEATbx).

   The Genetic and Evolutionary Algorithm Toolbox is not public domain.

   Copyright &#169; Hartmut Pohlheim, All Rights Reserved,

      (pohlheim@systemtechnik.tu-ilmenau.de).
