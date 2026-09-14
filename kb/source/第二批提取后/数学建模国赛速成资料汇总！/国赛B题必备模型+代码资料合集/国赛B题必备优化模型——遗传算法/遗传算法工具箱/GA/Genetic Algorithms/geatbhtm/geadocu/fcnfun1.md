GEATbx: Examples of Objective Functions

 Contents1.2 Axis parallel hyper-ellipsoid function

## 1 Parametric Optimization

### 1.1 De Jong's function 1

 The simplest test function is De Jong's function 1. It is continuos,

 convex and unimodal.

 function definition

 f1(x)=sum(x(i)^2),

 i=1:n;

 -5.12<=x(i)<=5.12.

 global minimum

 f(x)=0; x(i)=0, i=1:n.

 This function is implemented in objfun1.

GEA Toolbox: Main page | Tutorial | Algorithms | M-function index | Example functions

   This document is part of the Genetic and Evolutionary Algorithm Toolbox for use with Matlab (GEATbx).

   The Genetic and Evolutionary Algorithm Toolbox is not public domain.

   Copyright &#169; Hartmut Pohlheim, All Rights Reserved,

      (pohlheim@systemtechnik.tu-ilmenau.de).
