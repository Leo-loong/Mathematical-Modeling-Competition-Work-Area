GEATbx: Examples of Objective Functions

 1.3 Rotated hyper-ellipsoid function

 Contents1.5 Rastrigin's function 6

## 1 Parametric Optimization

### 1.4 Rosenbrock's valley (De

 Jong's function 2)

 Rosenbrock's valley is a classic optimization problem, also known

 as Banana function. The global optimum is inside a long, narrow,

 parabolic shaped flat valley. To find the valley is trivial, however

 convergence to the global optimum is difficult and hence this

 problem has been repeatedly used in assess the performance of

 optimization algorithms.

 function definition

 f2(x)=sum(100&#183;(x(i+1)-x(i)^2)^2+(1-x(i))^2),

 i=1:n-1;

 -2.048<=x(i)<=2.048.

 global minimum

 f(x)=0; x(i)=1, i=1:n.

 This function is implemented in objfun2.

GEA Toolbox: Main page | Tutorial | Algorithms | M-function index | Example functions

   This document is part of the Genetic and Evolutionary Algorithm Toolbox for use with Matlab (GEATbx).

   The Genetic and Evolutionary Algorithm Toolbox is not public domain.

   Copyright &#169; Hartmut Pohlheim, All Rights Reserved,

      (pohlheim@systemtechnik.tu-ilmenau.de).
