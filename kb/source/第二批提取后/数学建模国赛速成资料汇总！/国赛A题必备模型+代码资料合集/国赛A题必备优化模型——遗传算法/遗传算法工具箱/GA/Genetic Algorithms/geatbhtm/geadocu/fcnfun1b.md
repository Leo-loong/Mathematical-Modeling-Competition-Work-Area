GEATbx: Examples of Objective Functions

 1.2 Axis parallel hyper-ellipsoid function

 Contents1.4 Rosenbrock's valley (De Jong's function 2)

## 1 Parametric Optimization

### 1.3 Rotated hyper-ellipsoid

 function

 An extension of the axis parallel hyper-ellipsoid is Schwefel's

 function1.2. With respect to the coordinate axes, this function

 produces rotated hyper-ellipsoids. It is continuos, convex and

 unimodal.

 function definition

 f1b(x)=sum(sum(x(j)^2),

 j=1:i), i=1:n;

 -65.536<=x(i)<=65.536.

 global minimum

 f(x)=0; x(i)=0, i=1:n.

 This function is implemented in objfun1b.

GEA Toolbox: Main page | Tutorial | Algorithms | M-function index | Example functions

   This document is part of the Genetic and Evolutionary Algorithm Toolbox for use with Matlab (GEATbx).

   The Genetic and Evolutionary Algorithm Toolbox is not public domain.

   Copyright &#169; Hartmut Pohlheim, All Rights Reserved,

      (pohlheim@systemtechnik.tu-ilmenau.de).
