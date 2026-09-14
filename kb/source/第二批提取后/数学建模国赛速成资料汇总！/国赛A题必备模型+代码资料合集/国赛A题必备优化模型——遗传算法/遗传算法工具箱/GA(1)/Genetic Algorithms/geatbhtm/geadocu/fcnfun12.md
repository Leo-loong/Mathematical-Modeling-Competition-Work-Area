GEATbx: Examples of Objective Functions

 1.10 Langermann's function 11

 Contents1.12 Branins's rcos function

## 1 Parametric Optimization

### 1.11 Michalewicz's function

 12

 The Michalewicz function [Mic92]

 is a multimodal test function (n! local optima). The parameter

 m defines the &quot;steepness&quot; of the valleys

 or edges. Larger m leads to more difficult search.

 For very large m the function behaves like a needle

 in the haystack (the function values for points in the space outside

 the narrow peaks give very little information on the location

 of the global optimum).

 function definition

 f12(x)=-sum(sin(x(i))&#183;(sin(i&#183;x(i)^2/pi))^(2&#183;m)),

 i=1:n, m=10;

 0<=x(i)<=pi.

 global minimum

 f(x)=-4.687 (n=5); x(i)=???,

 i=1:n.

 f(x)=-9.66 (n=10); x(i)=???, i=1:n.

 This function is implemented in objfun12.

GEA Toolbox: Main page | Tutorial | Algorithms | M-function index | Example functions

   This document is part of the Genetic and Evolutionary Algorithm Toolbox for use with Matlab (GEATbx).

   The Genetic and Evolutionary Algorithm Toolbox is not public domain.

   Copyright &#169; Hartmut Pohlheim, All Rights Reserved,

      (pohlheim@systemtechnik.tu-ilmenau.de).
